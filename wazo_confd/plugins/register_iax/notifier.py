# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.register.event import (
    RegisterIAXCreatedEvent,
    RegisterIAXDeletedEvent,
    RegisterIAXEditedEvent,
)

from wazo_confd import bus, sysconfd


class RegisterIAXNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['iax2 reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, register):
        self.send_sysconfd_handlers()
        event = RegisterIAXCreatedEvent(register.id)
        self.bus.send_bus_event(event)

    def edited(self, register):
        self.send_sysconfd_handlers()
        event = RegisterIAXEditedEvent(register.id)
        self.bus.send_bus_event(event)

    def deleted(self, register):
        self.send_sysconfd_handlers()
        event = RegisterIAXDeletedEvent(register.id)
        self.bus.send_bus_event(event)


def build_notifier():
    return RegisterIAXNotifier(bus, sysconfd)
