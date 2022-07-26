# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.user.event import (
    CreateUserEvent,
    DeleteUserEvent,
    EditUserEvent,
    EditUserForwardEvent,
    EditUserServiceEvent,
)

from wazo_confd import bus, sysconfd


class UserNotifier:
    def __init__(self, sysconfd, bus):
        self.sysconfd = sysconfd
        self.bus = bus

    def send_sysconfd_handlers(self):
        handlers = {
            'ipbx': [
                'dialplan reload',
                'module reload chan_sccp.so',
                'module reload app_queue.so',
                'module reload res_pjsip.so',
            ],
        }
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, user):
        self.send_sysconfd_handlers()
        event = CreateUserEvent(
            user.id,
            user.uuid,
            subscription_type=user.subscription_type,
            created_at=user.created_at,
            tenant_uuid=user.tenant_uuid,
        )
        headers = self._build_headers(user)
        self.bus.send_bus_event(event, headers=headers)

    def edited(self, user):
        self.send_sysconfd_handlers()
        event = EditUserEvent(
            user.id,
            user.uuid,
            subscription_type=user.subscription_type,
            created_at=user.created_at,
            tenant_uuid=user.tenant_uuid,
        )
        headers = self._build_headers(user)
        self.bus.send_bus_event(event, headers=headers)

    def deleted(self, user):
        self.send_sysconfd_handlers()
        event = DeleteUserEvent(
            user.id,
            user.uuid,
            subscription_type=user.subscription_type,
            created_at=user.created_at,
            tenant_uuid=user.tenant_uuid,
        )
        headers = self._build_headers(user)
        self.bus.send_bus_event(event, headers=headers)

    def _build_headers(self, user):
        return {'tenant_uuid': str(user.tenant_uuid)}


def build_notifier():
    return UserNotifier(sysconfd, bus)


class UserServiceNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, user, schema):
        services = schema.dump(user)
        for type_ in schema.types:
            service = services.get(type_, services)
            event = EditUserServiceEvent(
                user.id, user.uuid, user.tenant_uuid, type_, service['enabled']
            )
            self.bus.send_bus_event(
                event,
                headers={
                    'user_uuid:{uuid}'.format(uuid=user.uuid): True,
                    'tenant_uuid': str(user.tenant_uuid),
                },
            )


def build_notifier_service():
    return UserServiceNotifier(bus)


class UserForwardNotifier:
    def __init__(self, bus):
        self.bus = bus

    def edited(self, user, schema):
        forwards = schema.dump(user)
        for type_ in schema.types:
            forward = forwards.get(type_, forwards)
            event = EditUserForwardEvent(
                user.id,
                user.uuid,
                str(user.tenant_uuid),
                type_,
                forward['enabled'],
                forward['destination'],
            )
            self.bus.send_bus_event(
                event,
                headers={
                    'user_uuid:{uuid}'.format(uuid=user.uuid): True,
                    'tenant_uuid': str(user.tenant_uuid),
                },
            )


def build_notifier_forward():
    return UserForwardNotifier(bus)
