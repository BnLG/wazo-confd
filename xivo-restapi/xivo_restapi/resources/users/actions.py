# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging

from flask import Blueprint
from flask.globals import request
from flask.helpers import make_response
from xivo_dao.data_handler.user import services as user_services
from xivo_dao.data_handler.user.model import User
from xivo_restapi.resources.users.mapper import UserMapper
from xivo_restapi.helpers import serializer
from xivo_dao.helpers.provd_connector import ProvdError
from xivo_dao.helpers.sysconfd_connector import SysconfdError
from xivo_restapi.helpers.route_generator import RouteGenerator
from xivo_restapi import config


logger = logging.getLogger(__name__)
blueprint = Blueprint('users', __name__, url_prefix='/%s/users' % config.VERSION_1_1)
route = RouteGenerator(blueprint)


@route('/')
def list():
    if 'q' in request.args:
        users = user_services.find_all_by_fullname(request.args['q'])
    else:
        users = user_services.find_all()

    result = UserMapper.encode(users)
    return make_response(result, 200)


@route('/<int:userid>')
def get(userid):
    user = user_services.get(userid)
    result = UserMapper.encode(user)
    return make_response(result, 200)


@route('/', methods=['POST'])
def create():
    data = request.data.decode("utf-8")
    data = serializer.decode(data)

    user = User.from_user_data(data)
    user = user_services.create(user)

    result = serializer.encode({
        'id': user.id
    })
    return make_response(result, 201)


@route('/<int:userid>', methods=['PUT'])
def edit(userid):
    data = request.data.decode("utf-8")
    data = serializer.decode(data)
    user = user_services.get(userid)
    user.update_from_data(data)
    user_services.edit(user)
    return make_response('', 204)


@route('/<int:userid>', methods=['DELETE'])
def delete(userid):
    user = user_services.get(userid)
    try:
        user_services.delete(user)
        return make_response('', 204)
    except ProvdError as e:
        result = "The user was deleted but the device could not be reconfigured (%s)" % str(e)
        result = serializer.encode([result])
        return make_response(result, 500)
    except SysconfdError as e:
        result = "The user was deleted but the voicemail content could not be removed (%s)" % str(e)
        result = serializer.encode([result])
        return make_response(result, 500)
