# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.endpoint_sccp.event import (
    CreateSccpEndpointEvent,
    DeleteSccpEndpointEvent,
    EditSccpEndpointEvent,
)

from wazo_confd import bus, sysconfd

from .schema import SccpSchema

ENDPOINT_SCCP_FIELDS = [
    'id',
    'tenant_uuid',
    'line.id',
]


class SccpEndpointNotifier:
    def __init__(self, sysconfd, bus):
        self.sysconfd = sysconfd
        self.bus = bus

    def send_sysconfd_handlers(self):
        handlers = {
            'ipbx': ['module reload chan_sccp.so', 'dialplan reload'],
            'agentbus': [],
        }
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, sccp):
        sccp_serialized = SccpSchema(only=ENDPOINT_SCCP_FIELDS).dump(sccp)
        event = CreateSccpEndpointEvent(sccp_serialized)
        headers = self._build_headers(sccp)
        self.bus.send_bus_event(event, headers=headers)

    def edited(self, sccp):
        sccp_serialized = SccpSchema(only=ENDPOINT_SCCP_FIELDS).dump(sccp)
        self.send_sysconfd_handlers()
        event = EditSccpEndpointEvent(sccp_serialized)
        headers = self._build_headers(sccp)
        self.bus.send_bus_event(event, headers=headers)

    def deleted(self, sccp):
        sccp_serialized = SccpSchema(only=ENDPOINT_SCCP_FIELDS).dump(sccp)
        self.send_sysconfd_handlers()
        event = DeleteSccpEndpointEvent(sccp_serialized)
        headers = self._build_headers(sccp)
        self.bus.send_bus_event(event, headers=headers)

    def _build_headers(self, sccp):
        return {'tenant_uuid': str(sccp.tenant_uuid)}


def build_notifier():
    return SccpEndpointNotifier(sysconfd, bus)
