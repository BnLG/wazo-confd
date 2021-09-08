# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from . import confd


def generate_conference(**parameters):
    return add_conference(**parameters)


def add_conference(wazo_tenant=None, **parameters):
    response = confd.conferences.post(parameters, wazo_tenant=wazo_tenant)
    return response.item


def delete_conference(conference_id, check=False, **params):
    response = confd.conferences(conference_id).delete()
    if check:
        response.assert_ok()
