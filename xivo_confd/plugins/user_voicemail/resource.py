# -*- coding: UTF-8 -*-
# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.helpers.exception import NotFoundError
from xivo_dao.helpers import errors

from flask import url_for, request
from marshmallow import fields

from xivo_confd.authentication.confd_auth import required_acl
from xivo_confd.helpers.mallow import BaseSchema, Link, ListLink
from xivo_confd.helpers.restful import ConfdResource


class UserVoicemailSchema(BaseSchema):
    user_id = fields.Integer(dump_only=True)
    voicemail_id = fields.Integer(required=True)
    links = ListLink(Link('voicemails',
                          field='voicemail_id',
                          target='id'),
                     Link('users',
                          field='user_id',
                          target='id'))


class UserVoicemailResource(ConfdResource):

    schema = UserVoicemailSchema

    def __init__(self, service, user_dao, voicemail_dao):
        super(UserVoicemailResource, self).__init__()
        self.service = service
        self.user_dao = user_dao
        self.voicemail_dao = voicemail_dao

    def get_user(self, user_id):
        return self.user_dao.get_by_id_uuid(user_id)


class UserVoicemailItem(UserVoicemailResource):

    @required_acl('confd.users.{user_id}.voicemails.{voicemail_id}.update')
    def put(self, user_id, voicemail_id):
        user = self.get_user(user_id)
        voicemail = self.voicemail_dao.get(voicemail_id)
        self.service.associate(user, voicemail)
        return '', 204


class UserVoicemailList(UserVoicemailResource):

    @required_acl('confd.users.{user_id}.voicemails.read')
    def get(self, user_id):
        user = self.get_user(user_id)
        user_voicemail = self.service.get_by(user_id=user.id)
        return self.schema().dump(user_voicemail).data

    @required_acl('confd.users.{user_id}.voicemails.delete')
    def delete(self, user_id):
        user = self.get_user(user_id)
        self.service.dissociate_all_by_user(user)
        return '', 204


class VoicemailUserList(UserVoicemailResource):

    @required_acl('confd.voicemails.{voicemail_id}.users.read')
    def get(self, voicemail_id):
        voicemail = self.voicemail_dao.get(voicemail_id)
        items = self.service.find_all_by(voicemail_id=voicemail.id)
        return {'total': len(items),
                'items': self.schema().dump(items, many=True).data}


class UserVoicemailLegacy(UserVoicemailResource):

    @required_acl('confd.users.{user_id}.voicemail.read')
    def get(self, user_id):
        user = self.get_user(user_id)
        user_voicemail = self.service.get_by(user_id=user.id)
        return self.schema().dump(user_voicemail).data

    @required_acl('confd.users.{user_id}.voicemail.create')
    def post(self, user_id):
        user = self.get_user(user_id)
        voicemail = self.get_voicemail_or_fail()
        user_voicemail = self.service.associate(user, voicemail)
        return self.schema().dump(user_voicemail).data, 201, self.build_headers(user_voicemail)

    @required_acl('confd.users.{user_id}.voicemail.delete')
    def delete(self, user_id):
        user = self.get_user(user_id)
        user_voicemail = self.service.get_by(user_id=user.id)
        voicemail = self.voicemail_dao.get(user_voicemail.voicemail_id)
        self.service.dissociate(user, voicemail)
        return '', 204

    def build_headers(self, model):
        url = url_for('user_voicemails',
                      user_id=model.user_id,
                      voicemail_id=model.voicemail_id,
                      _external=True)
        return {'Location': url}

    def get_voicemail_or_fail(self):
        form = self.schema().load(request.get_json()).data
        try:
            return self.voicemail_dao.get(form['voicemail_id'])
        except NotFoundError:
            raise errors.param_not_found('voicemail_id', 'Voicemail')
