# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.application.event import (
    ApplicationCreatedEvent,
    ApplicationDeletedEvent,
    ApplicationEditedEvent,
)

from wazo_confd import bus

from .schema import ApplicationSchema

APPLICATION_FIELDS = [
    'uuid',
    'tenant_uuid',
    'name',
    'destination',
    'destination_options',
]


class ApplicationNotifier:
    def __init__(self, bus):
        self.bus = bus

    def created(self, application):
        app_serialized = ApplicationSchema(only=APPLICATION_FIELDS).dump(application)
        event = ApplicationCreatedEvent(app_serialized, application.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, application):
        app_serialized = ApplicationSchema(only=APPLICATION_FIELDS).dump(application)
        event = ApplicationEditedEvent(app_serialized, application.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, application):
        app_serialized = ApplicationSchema(only=APPLICATION_FIELDS).dump(application)
        event = ApplicationDeletedEvent(app_serialized, application.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return ApplicationNotifier(bus)
