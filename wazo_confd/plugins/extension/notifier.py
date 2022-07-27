# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.extension.event import (
    CreateExtensionEvent,
    DeleteExtensionEvent,
    EditExtensionEvent,
)

from wazo_confd import bus, sysconfd


class ExtensionNotifier:
    def __init__(self, sysconfd, bus):
        self.sysconfd = sysconfd
        self.bus = bus

    def send_sysconfd_handlers(self, ipbx):
        handlers = {'ipbx': ipbx}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, extension):
        self.send_sysconfd_handlers(['dialplan reload'])
        event = CreateExtensionEvent(extension.id, extension.exten, extension.context)
        headers = self._build_headers(extension)
        self.bus.send_bus_event(event, headers=headers)

    def edited(self, extension, updated_fields):
        if updated_fields is None or updated_fields:
            self.send_sysconfd_handlers(
                [
                    'dialplan reload',
                    'module reload res_pjsip.so',
                    'module reload chan_sccp.so',
                    'module reload app_queue.so',
                ]
            )
        event = EditExtensionEvent(extension.id, extension.exten, extension.context)
        headers = self._build_headers(extension)
        self.bus.send_bus_event(event, headers=headers)

    def deleted(self, extension):
        self.send_sysconfd_handlers(['dialplan reload'])
        event = DeleteExtensionEvent(extension.id, extension.exten, extension.context)
        headers = self._build_headers(extension)
        self.bus.send_bus_event(event, headers=headers)

    def _build_headers(self, extension):
        return {'tenant_uuid': str(extension.tenant_uuid)}


def build_notifier():
    return ExtensionNotifier(sysconfd, bus)
