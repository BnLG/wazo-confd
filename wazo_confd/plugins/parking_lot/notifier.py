# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.parking_lot.event import (
    ParkingLotCreatedEvent,
    ParkingLotDeletedEvent,
    ParkingLotEditedEvent,
)

from wazo_confd import bus, sysconfd


class ParkingLotNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def send_sysconfd_handlers(self):
        handlers = {'ipbx': ['module reload res_parking.so']}
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, parking_lot):
        self.send_sysconfd_handlers()
        event = ParkingLotCreatedEvent(parking_lot.id, parking_lot.tenant_uuid)
        self.bus.queue_event(event)

    def edited(self, parking_lot):
        self.send_sysconfd_handlers()
        event = ParkingLotEditedEvent(parking_lot.id, parking_lot.tenant_uuid)
        self.bus.queue_event(event)

    def deleted(self, parking_lot):
        self.send_sysconfd_handlers()
        event = ParkingLotDeletedEvent(parking_lot.id, parking_lot.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return ParkingLotNotifier(bus, sysconfd)
