# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from marshmallow import fields
from marshmallow.validate import Regexp

from wazo_confd.helpers.mallow import BaseSchema, Link, ListLink
from wazo_confd.helpers.validator import EXTEN_REGEX


class ExtensionFeatureSchema(BaseSchema):
    uuid = fields.UUID(dump_only=True)
    exten = fields.String(validate=Regexp(EXTEN_REGEX), required=True)
    context = fields.String(dump_only=True)
    feature = fields.String(dump_only=True)
    enabled = fields.Boolean()
    links = ListLink(Link('extensions_features', field='uuid'))
