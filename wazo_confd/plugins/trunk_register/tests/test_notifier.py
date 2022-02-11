# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from uuid import uuid4
from mock import Mock
from xivo_bus.resources.trunk_register.event import (
    TrunkRegisterIAXAssociatedEvent,
    TrunkRegisterIAXDissociatedEvent,
)
from xivo_dao.alchemy.trunkfeatures import TrunkFeatures as Trunk

from ..notifier import TrunkRegisterIAXNotifier


class TestTrunkRegisterIAXNotifier(unittest.TestCase):
    def setUp(self):
        self.bus = Mock()
        self.iax = Mock(id=2)
        self.trunk = Mock(Trunk, id=3, tenant_uuid=uuid4())
        self.expected_headers = {'tenant_uuid': str(self.trunk.tenant_uuid)}

        self.notifier_iax = TrunkRegisterIAXNotifier(self.bus)

    def test_associate_iax_then_bus_event(self):
        expected_event = TrunkRegisterIAXAssociatedEvent(self.trunk.id, self.iax.id)

        self.notifier_iax.associated(self.trunk, self.iax)

        self.bus.send_bus_event.assert_called_once_with(
            expected_event, headers=self.expected_headers
        )

    def test_dissociate_iax_then_bus_event(self):
        expected_event = TrunkRegisterIAXDissociatedEvent(self.trunk.id, self.iax.id)

        self.notifier_iax.dissociated(self.trunk, self.iax)

        self.bus.send_bus_event.assert_called_once_with(
            expected_event, headers=self.expected_headers
        )
