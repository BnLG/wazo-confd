# -*- coding: UTF-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from .resource import ConfBridgeDefaultBridgeList, ConfBridgeDefaultUserList
from .service import build_service


class Plugin(object):

    def load(self, core):
        api = core.api
        service = build_service()

        api.add_resource(
            ConfBridgeDefaultBridgeList,
            '/asterisk/confbridge/default_bridge',
            resource_class_args=(service,)
        )

        api.add_resource(
            ConfBridgeDefaultUserList,
            '/asterisk/confbridge/default_user',
            resource_class_args=(service,)
        )
