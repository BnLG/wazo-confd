# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .resource import GroupItem, GroupList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(GroupList, '/groups', resource_class_args=(service,))

        api.add_resource(
            GroupItem,
            '/groups/<uuid:id>',
            '/groups/<int:id>',
            endpoint='groups',
            resource_class_args=(service,),
        )
