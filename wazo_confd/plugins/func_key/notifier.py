# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.func_key.event import (
    FuncKeyTemplateCreatedEvent,
    FuncKeyTemplateDeletedEvent,
    FuncKeyTemplateEditedEvent,
)

from wazo_confd import bus, sysconfd
from wazo_confd.database import device as device_db_module


class FuncKeyTemplateNotifier:
    def __init__(self, bus, sysconfd, device_db):
        self.bus = bus
        self.sysconfd = sysconfd
        self.device_db = device_db

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, template):
        event = FuncKeyTemplateCreatedEvent(template.id, template.tenant_uuid)
        self.bus.send_bus_event(event)

    def edited(self, template, updated_fields):
        event = FuncKeyTemplateEditedEvent(template.id, template.tenant_uuid)
        self.bus.send_bus_event(event)
        if updated_fields is None or updated_fields:
            self.send_sysconfd_handlers(['dialplan reload'])
            self._reload_sccp(template)

    def deleted(self, template):
        event = FuncKeyTemplateDeletedEvent(template.id, template.tenant_uuid)
        self.bus.send_bus_event(event)
        self.send_sysconfd_handlers(['dialplan reload'])
        self._reload_sccp(template)

    def _reload_sccp(self, template):
        if self.device_db.template_has_sccp_device(template.id):
            self.send_sysconfd_handlers(['module reload chan_sccp.so'])


def build_notifier():
    return FuncKeyTemplateNotifier(bus, sysconfd, device_db_module)
