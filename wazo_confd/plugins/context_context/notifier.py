# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.context_context.event import ContextContextsAssociatedEvent

from wazo_confd import bus, sysconfd


class ContextContextNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['dialplan reload']}
        self.sysconfd.exec_request_handlers(handlers)

    def associated_contexts(self, context, contexts):
        self.send_sysconfd_handlers()
        context_ids = [context.id for context in contexts]
        event = ContextContextsAssociatedEvent(
            context.id, context_ids, context.tenant_uuid
        )
        self.bus.send_bus_event(event)


def build_notifier():
    return ContextContextNotifier(bus, sysconfd)
