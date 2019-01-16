# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    contains,
    empty,
    has_entries,
)

from . import confd
from ..helpers import (
    associations as a,
    errors as e,
    fixtures,
    scenarios as s,
)
from ..helpers.config import (
    MAIN_TENANT,
    SUB_TENANT,
)

FAKE_ID = 999999999
FAKE_UUID = '99999999-9999-9999-9999-999999999999'


@fixtures.call_filter()
@fixtures.user()
def test_associate_errors(call_filter, user):
    response = confd.callfilters(FAKE_ID).recipients.users.put(users=[user])
    response.assert_status(404)

    url = confd.callfilters(call_filter['id']).recipients.users.put
    for check in error_checks(url):
        yield check


def error_checks(url):
    yield s.check_bogus_field_returns_error, url, 'users', 123
    yield s.check_bogus_field_returns_error, url, 'users', None
    yield s.check_bogus_field_returns_error, url, 'users', True
    yield s.check_bogus_field_returns_error, url, 'users', 'string'
    yield s.check_bogus_field_returns_error, url, 'users', [123]
    yield s.check_bogus_field_returns_error, url, 'users', [None]
    yield s.check_bogus_field_returns_error, url, 'users', ['string']
    yield s.check_bogus_field_returns_error, url, 'users', [{}]
    yield s.check_bogus_field_returns_error, url, 'users', [{'uuid': None}]
    yield s.check_bogus_field_returns_error, url, 'users', [{'uuid': 1}, {'uuid': None}]
    yield s.check_bogus_field_returns_error, url, 'users', [{'not_uuid': 123}]
    yield s.check_bogus_field_returns_error, url, 'users', [{'uuid': FAKE_UUID}]

    regex = r'users.*timeout'
    yield s.check_bogus_field_returns_error_matching_regex, url, 'users', [{'timeout': 'ten'}], regex
    yield s.check_bogus_field_returns_error_matching_regex, url, 'users', [{'timeout': -1}], regex
    yield s.check_bogus_field_returns_error_matching_regex, url, 'users', [{'timeout': {}}], regex
    yield s.check_bogus_field_returns_error_matching_regex, url, 'users', [{'timeout': []}], regex


@fixtures.call_filter()
@fixtures.user()
def test_associate(call_filter, user):
    response = confd.callfilters(call_filter['id']).recipients.users.put(users=[user])
    response.assert_updated()


@fixtures.call_filter()
@fixtures.user()
@fixtures.user()
def test_associate_more_than_one_recipient(call_filter, user1, user2):
    response = confd.callfilters(call_filter['id']).recipients.users.put(users=[user1, user2])
    response.assert_status(400)


@fixtures.call_filter()
@fixtures.user()
def test_associate_surrogate_to_recipient(call_filter, user):
    with a.call_filter_surrogate_user(call_filter, user):
        response = confd.callfilters(call_filter['id']).recipients.users.put(users=[user])
        response.assert_status(400)


@fixtures.call_filter(wazo_tenant=MAIN_TENANT)
@fixtures.call_filter(wazo_tenant=SUB_TENANT)
@fixtures.user(wazo_tenant=MAIN_TENANT)
@fixtures.user(wazo_tenant=SUB_TENANT)
def test_associate_multi_tenant(main_call_filter, sub_call_filter, main_user, sub_user):
    response = confd.callfilters(main_call_filter['id']).recipients.users.put(
        users=[{'uuid': main_user['uuid']}],
        wazo_tenant=SUB_TENANT,
    )
    response.assert_match(404, e.not_found('CallFilter'))

    response = confd.callfilters(sub_call_filter['id']).recipients.users.put(
        users=[{'uuid': main_user['uuid']}],
        wazo_tenant=SUB_TENANT,
    )
    response.assert_match(400, e.not_found('User'))

    response = confd.callfilters(main_call_filter['id']).recipients.users.put(
        users=[{'uuid': sub_user['uuid']}],
        wazo_tenant=MAIN_TENANT,
    )
    response.assert_match(400, e.different_tenant())


@fixtures.call_filter()
@fixtures.user()
def test_get_users_associated_to_call_filter(call_filter, user):
    with a.call_filter_recipient_user(call_filter, user):
        response = confd.callfilters(call_filter['id']).get()
        assert_that(response.item, has_entries(
            recipients=has_entries(users=contains(
                has_entries(
                    uuid=user['uuid'],
                    firstname=user['firstname'],
                    lastname=user['lastname'],
                ),
            ))
        ))


@fixtures.call_filter()
@fixtures.user()
def test_dissociate(call_filter, user):
    with a.call_filter_recipient_user(call_filter, user):
        response = confd.callfilters(call_filter['id']).recipients.users.put(users=[])
        response.assert_updated()


@fixtures.call_filter()
@fixtures.user()
@fixtures.user()
def test_delete_call_filter_when_call_filter_and_user_associated(call_filter, user1, user2):
    with a.call_filter_recipient_user(call_filter, user1, user2, check=False):
        confd.callfilters(call_filter['id']).delete().assert_deleted()

        deleted_call_filter = confd.callfilters(call_filter['id']).get
        yield s.check_resource_not_found, deleted_call_filter, 'CallFilter'

        # When the relation will be added,
        # we should check if users have the key.callfilters to empty


@fixtures.call_filter()
@fixtures.call_filter()
@fixtures.user()
def test_delete_user_when_call_filter_and_user_associated(call_filter1, call_filter2, user):
    with a.call_filter_recipient_user(call_filter1, user, check=False), \
            a.call_filter_recipient_user(call_filter2, user, check=False):
        confd.users(user['uuid']).delete().assert_deleted()

        response = confd.callfilters(call_filter1['id']).get()
        yield assert_that, response.item['recipients']['users'], empty()

        response = confd.callfilters(call_filter2['id']).get()
        yield assert_that, response.item['recipients']['users'], empty()


@fixtures.call_filter()
@fixtures.user()
def test_bus_events(call_filter, user):
    url = confd.callfilters(call_filter['id']).recipients.users.put
    body = {'users': [user]}
    yield s.check_bus_event, 'config.callfilters.recipients.users.updated', url, body
