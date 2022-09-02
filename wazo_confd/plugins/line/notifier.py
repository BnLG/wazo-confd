# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.line.event import (
    LineCreatedEvent,
    LineDeletedEvent,
    LineEditedEvent,
)

from wazo_confd import bus, sysconfd
from wazo_confd.plugins.line.schema import LineSchema

LINE_FIELDS = [
    'id',
    'protocol',
    'name',
    'tenant_uuid',
]


class LineNotifier:
    def __init__(self, sysconfd, bus):
        self.sysconfd = sysconfd
        self.bus = bus

    def send_sysconfd_handlers(self):
        handlers = {
            'ipbx': [
                'module reload res_pjsip.so',
                'dialplan reload',
                'module reload chan_sccp.so',
            ],
        }
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, line):
        self.send_sysconfd_handlers()
        serialized_line = LineSchema(only=LINE_FIELDS).dump(line)
        event = LineCreatedEvent(serialized_line, line.tenant_uuid)
        self.bus.send_bus_event(event)

    def edited(self, line, updated_fields):
        if updated_fields is None or updated_fields:
            self.send_sysconfd_handlers()
        serialized_line = LineSchema(only=LINE_FIELDS).dump(line)
        event = LineEditedEvent(serialized_line, line.tenant_uuid)
        self.bus.send_bus_event(event)

    def deleted(self, line):
        self.send_sysconfd_handlers()
        serialized_line = LineSchema(only=LINE_FIELDS).dump(line)
        event = LineDeletedEvent(serialized_line, line.tenant_uuid)
        self.bus.send_bus_event(event)


def build_notifier():
    return LineNotifier(sysconfd, bus)
