# -*- coding: UTF-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from hamcrest import assert_that, has_items, has_entries

from test_api import confd
from test_api import fixtures
from test_api import associations as a


@fixtures.user()
@fixtures.line()
@fixtures.extension()
def test_associate_user_then_line_then_extension(user, line, extension):
    response = confd.users(user['id']).lines.post(line_id=line['id'])
    response.assert_ok()

    response = confd.lines(line['id']).extensions.post(extension_id=extension['id'])
    response.assert_ok()


@fixtures.user()
@fixtures.line()
@fixtures.extension()
def test_associate_extension_then_line_then_user(user, line, extension):
    response = confd.lines(line['id']).extensions.post(extension_id=extension['id'])
    response.assert_ok()

    response = confd.users(user['id']).lines.post(line_id=line['id'])
    response.assert_ok()


@fixtures.user()
@fixtures.line()
@fixtures.extension()
def test_dissociate_user_then_line_then_extension(user, line, extension):
    with a.user_line(user, line, check=False), a.line_extension(line, extension, check=False):

        response = confd.users(user['id']).lines(line['id']).delete()
        response.assert_ok()

        response = confd.lines(line['id']).extensions(extension['id']).delete()
        response.assert_ok()


@fixtures.user()
@fixtures.line()
@fixtures.extension()
def test_dissociate_extension_then_line_then_user(user, line, extension):
    with a.user_line(user, line, check=False), a.line_extension(line, extension, check=False):

        response = confd.lines(line['id']).extensions(extension['id']).delete()
        response.assert_ok()

        response = confd.users(user['id']).lines(line['id']).delete()
        response.assert_ok()


@fixtures.user()
@fixtures.line()
@fixtures.extension(context='default')
@fixtures.extension(context='from-extern')
def test_get_line_extension_associations(user, line, internal, incall):
    expected = has_items(has_entries({'line_id': line['id'],
                                     'extension_id': internal['id']}),
                         has_entries({'line_id': line['id'],
                                      'extension_id': incall['id']})
                         )

    with a.user_line(user, line), a.line_extension(line, internal), a.line_extension(line, incall):
        response = confd.lines(line['id']).extensions.get()
        assert_that(response.items, expected)


@fixtures.user()
@fixtures.line()
@fixtures.extension(context='default')
@fixtures.extension(context='from-extern')
def test_associate_line_and_incall(user, line, internal, incall):
    expected = has_entries({'line_id': line['id'],
                            'extension_id': incall['id']})

    with a.user_line(user, line):
        response = confd.lines(line['id']).extensions.post(extension_id=incall['id'])
        assert_that(response.item, expected)


@fixtures.user()
@fixtures.line()
@fixtures.extension(context='default')
@fixtures.extension(context='from-extern')
def test_dissociate_line_and_incall(user, line, internal, incall):
    with a.user_line(user, line), a.line_extension(line, incall, check=False):
        response = confd.lines(line['id']).extensions(incall['id']).delete()
        response.assert_ok()
