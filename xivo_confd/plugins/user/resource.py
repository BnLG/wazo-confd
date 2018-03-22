# -*- coding: utf-8 -*-
# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import url_for, request

from xivo_dao.alchemy.userfeatures import UserFeatures as User

from xivo_confd.auth import required_acl
from xivo_confd.helpers.restful import ListResource, ItemResource

from .schema import (
    UserDirectorySchema,
    UserSchema,
    UserSchemaNullable,
    UserSummarySchema,
)


class UserList(ListResource):

    model = User
    schema = UserSchemaNullable
    view_schemas = {'directory': UserDirectorySchema,
                    'summary': UserSummarySchema}

    def __init__(self, service, auth_token_cache, auth_user_cache):
        self.auth_token_cache = auth_token_cache
        self.auth_user_cache = auth_user_cache
        super(UserList, self).__init__(service)

    def build_headers(self, user):
        return {'Location': url_for('users', id=user.id, _external=True)}

    @required_acl('confd.users.create')
    def post(self):
        return super(UserList, self).post()

    @required_acl('confd.users.read')
    def get(self):
        tenant_uuids = self._get_tenant_uuids()
        if 'q' in request.args:
            return self.legacy_search(tenant_uuids=tenant_uuids)
        else:
            return self.user_search(tenant_uuids=tenant_uuids)

    def legacy_search(self, tenant_uuids=None):
        result = self.service.legacy_search(request.args['q'], tenant_uuids=tenant_uuids)
        return {'total': result.total,
                'items': self.schema().dump(result.items, many=True).data}

    def user_search(self, tenant_uuids=None):
        view = request.args.get('view')
        schema = self.view_schemas.get(view, self.schema)
        params = self.search_params()
        result = self.service.search(params, tenant_uuids)
        return {'total': result.total,
                'items': schema().dump(result.items, many=True).data}

    def _get_tenant_uuids(self):
        token = request.headers['X-Auth-Token']
        token_data = self.auth_token_cache._auth.token.get(token)
        return [tenant['uuid'] for tenant in token_data['metadata']['tenants']]


class UserItem(ItemResource):

    schema = UserSchema

    def __init__(self, service, auth_token_cache, auth_user_cache):
        self.auth_token_cache = auth_token_cache
        self.auth_user_cache = auth_user_cache
        super(UserItem, self).__init__(service)

    @required_acl('confd.users.{id}.read')
    def head(self, id):
        tenant_uuids = self._get_tenant_uuids()
        self.service.get(id, tenant_uuids=tenant_uuids)
        return '', 200

    @required_acl('confd.users.{id}.read')
    def get(self, id):
        return super(UserItem, self).get(id)

    @required_acl('confd.users.{id}.update')
    def put(self, id):
        return super(UserItem, self).put(id)

    @required_acl('confd.users.{id}.delete')
    def delete(self, id):
        return super(UserItem, self).delete(id)
