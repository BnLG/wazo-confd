# -*- coding: utf-8 -*-

# Copyright 2016-2017 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

from ..helpers import scenarios as s
from ..helpers import errors as e
from ..helpers import fixtures
from . import confd

from hamcrest import (assert_that,
                      has_entries,
                      has_entry,
                      has_item,
                      is_not)


def test_get_errors():
    fake_get = confd.callpermissions(999999).get
    yield s.check_resource_not_found, fake_get, 'CallPermission'


def test_post_errors():
    url = confd.callpermissions.post
    for check in error_checks(url):
        yield check


@fixtures.call_permission()
def test_put_errors(call_permission):
    url = confd.callpermissions(call_permission['id']).put
    for check in error_checks(url):
        yield check


def error_checks(url):
    yield s.check_bogus_field_returns_error, url, 'name', 123
    yield s.check_bogus_field_returns_error, url, 'name', None
    yield s.check_bogus_field_returns_error, url, 'name', True
    yield s.check_bogus_field_returns_error, url, 'name', 'invalid_régèx!'
    yield s.check_bogus_field_returns_error, url, 'name', {}
    yield s.check_bogus_field_returns_error, url, 'name', []
    yield s.check_bogus_field_returns_error, url, 'password', 123
    yield s.check_bogus_field_returns_error, url, 'password', True
    yield s.check_bogus_field_returns_error, url, 'password', 'invalid'
    yield s.check_bogus_field_returns_error, url, 'password', {}
    yield s.check_bogus_field_returns_error, url, 'password', []
    yield s.check_bogus_field_returns_error, url, 'description', 123
    yield s.check_bogus_field_returns_error, url, 'description', True
    yield s.check_bogus_field_returns_error, url, 'description', {}
    yield s.check_bogus_field_returns_error, url, 'description', []
    yield s.check_bogus_field_returns_error, url, 'mode', 123
    yield s.check_bogus_field_returns_error, url, 'mode', None
    yield s.check_bogus_field_returns_error, url, 'mode', False
    yield s.check_bogus_field_returns_error, url, 'mode', 'invalid'
    yield s.check_bogus_field_returns_error, url, 'enabled', None
    yield s.check_bogus_field_returns_error, url, 'enabled', 123
    yield s.check_bogus_field_returns_error, url, 'enabled', 'invalid'
    yield s.check_bogus_field_returns_error, url, 'enabled', {}
    yield s.check_bogus_field_returns_error, url, 'enabled', []
    yield s.check_bogus_field_returns_error, url, 'extensions', 'invalid'
    yield s.check_bogus_field_returns_error, url, 'extensions', 123
    yield s.check_bogus_field_returns_error, url, 'extensions', True
    yield s.check_bogus_field_returns_error, url, 'extensions', None
    yield s.check_bogus_field_returns_error, url, 'extensions', {}


@fixtures.call_permission(name="search",
                          password="123",
                          description="SearchDesc",
                          mode='deny',
                          enabled=True)
@fixtures.call_permission(name="hidden",
                          password="456",
                          description="HiddenDesc",
                          mode='allow',
                          enabled=False)
def test_search_on_call_permission(call_permission, hidden):
    url = confd.callpermissions
    searches = {'name': 'search',
                'description': 'Search',
                'mode': 'deny',
                'enabled': True}

    for field, term in searches.items():
        yield check_search, url, call_permission, hidden, field, term


@fixtures.call_permission(name="sort1",
                          description="Sort 1")
@fixtures.call_permission(name="sort2",
                          description="Sort 2")
def test_sorting_offset_limit(call_permission1, call_permission2):
    url = confd.callpermissions.get
    yield s.check_sorting, url, call_permission1, call_permission2, 'name', 'sort'
    yield s.check_sorting, url, call_permission1, call_permission2, 'description', 'Sort'

    yield s.check_offset, url, call_permission1, call_permission2, 'name', 'sort'
    yield s.check_offset_legacy, url, call_permission1, call_permission2, 'name', 'sort'

    yield s.check_limit, url, call_permission1, call_permission2, 'name', 'sort'


def check_search(url, call_permission, hidden, field, term):
    response = url.get(search=term)

    expected_call_permission = has_item(has_entry(field, call_permission[field]))
    hidden_call_permission = is_not(has_item(has_entry(field, hidden[field])))
    assert_that(response.items, expected_call_permission)
    assert_that(response.items, hidden_call_permission)

    response = url.get(**{field: call_permission[field]})

    expected_call_permission = has_item(has_entry('id', call_permission['id']))
    hidden_call_permission = is_not(has_item(has_entry('id', hidden['id'])))
    assert_that(response.items, expected_call_permission)
    assert_that(response.items, hidden_call_permission)


@fixtures.call_permission(name="search",
                          password="123",
                          description="SearchDesc",
                          mode='deny',
                          enabled=True,
                          extensions=['123', '456'])
def test_get(call_permission):
    response = confd.callpermissions(call_permission['id']).get()
    assert_that(response.item, has_entries(name='search',
                                           password='123',
                                           description='SearchDesc',
                                           mode='deny',
                                           enabled=True,
                                           extensions=['123', '456']))


def test_create_call_permission_minimal_parameters():
    response = confd.callpermissions.post(name='minimal')
    response.assert_created('callpermissions')

    assert_that(response.item, has_entries(name='minimal',
                                           password=None,
                                           description=None,
                                           mode='deny',
                                           enabled=True,
                                           extensions=[]))


def test_create_call_permission_all_parameters():
    parameters = {'name': 'allparameter',
                  'password': '1234',
                  'description': 'Create description',
                  'mode': 'allow',
                  'enabled': False,
                  'extensions': ['123', '*456', '963']}

    response = confd.callpermissions.post(**parameters)
    response.assert_created('callpermissions')
    assert_that(response.item, has_entries(parameters))


def test_create_call_permission_without_name():
    response = confd.callpermissions.post()
    response.assert_status(400)


@fixtures.call_permission()
def test_create_2_call_permissions_with_same_name(call_permission):
    response = confd.callpermissions.post(name=call_permission['name'])
    response.assert_match(400, e.resource_exists('CallPermission'))


@fixtures.call_permission()
def test_create_call_permissions_with_invalid_mode(call_permission):
    response = confd.callpermissions.post(name=call_permission['name'], mode='invalidmode')
    response.assert_status(400)


def test_create_call_permissions_with_duplicate_extensions():
    parameters = {'name': 'duplicate_perm',
                  'extensions': ['123', '123', '456']}

    response = confd.callpermissions.post(**parameters)
    response.assert_created('callpermissions')
    assert_that(response.item, has_entries(name=parameters['name'],
                                           extensions=['123', '456']))


@fixtures.call_permission(name='name1', extension=['123'])
def test_edit_call_permission_all_parameters(call_permission):
    parameters = {'name': 'second',
                  'password': '1234',
                  'description': 'Create description',
                  'mode': 'allow',
                  'enabled': False,
                  'extensions': ['123', '*456', '963']}

    response = confd.callpermissions(call_permission['id']).put(**parameters)
    response.assert_updated()

    response = confd.callpermissions(call_permission['id']).get()
    assert_that(response.item, has_entries(parameters))


@fixtures.call_permission(name='call_permission1')
@fixtures.call_permission(name='call_permission2')
def test_edit_call_permission_with_same_name(first_call_permission, second_call_permission):
    response = confd.callpermissions(first_call_permission['id']).put(name=second_call_permission['name'])
    response.assert_match(400, e.resource_exists('CallPermission'))


@fixtures.call_permission()
def test_delete_call_permission(call_permission):
    response = confd.callpermissions(call_permission['id']).delete()
    response.assert_deleted()
