# -*- coding: UTF-8 -*-
# Copyright 2016-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from .resource import Info
from .service import build_service


class Plugin(object):

    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            Info,
            '/infos',
            resource_class_args=(service,)
        )
