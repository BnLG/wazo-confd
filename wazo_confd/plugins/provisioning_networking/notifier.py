# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.provisioning_networking.event import (
    ProvisioningNetworkingEditedEvent,
)


class ProvisioningNetworkingNotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def edited(self, provisioning_networking):
        event = ProvisioningNetworkingEditedEvent()
        self.bus.send_bus_event(event)
        self.sysconfd.commonconf_generate()
        self.sysconfd.commonconf_apply()
        self.sysconfd.restart_provd()
