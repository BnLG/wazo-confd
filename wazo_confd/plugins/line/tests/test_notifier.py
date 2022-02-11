# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from uuid import uuid4
from mock import Mock

from xivo_bus.resources.line.event import (
    CreateLineEvent,
    DeleteLineEvent,
    EditLineEvent,
)
from xivo_dao.alchemy.linefeatures import LineFeatures as Line

from ..notifier import LineNotifier

SYSCONFD_HANDLERS = {
    'ipbx': [
        'module reload res_pjsip.so',
        'dialplan reload',
        'module reload chan_sccp.so',
    ],
    'agentbus': [],
}


class TestLineNotifier(unittest.TestCase):
    def setUp(self):
        self.sysconfd = Mock()
        self.bus = Mock()
        self.line = Mock(Line, id=1234, protocol='sip', tenant_uuid=uuid4())
        self.line.name = 'limitation of mock instantiation with name ...'
        self.line_serialized = {
            'id': self.line.id,
            'name': self.line.name,
            'tenant_uuid': str(self.line.tenant_uuid),
            'protocol': self.line.protocol,
        }
        self.expected_headers = {'tenant_uuid': str(self.line.tenant_uuid)}

        self.notifier = LineNotifier(self.sysconfd, self.bus)

    def test_when_line_created_then_sip_reloaded(self):
        self.notifier.created(self.line)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_when_line_created_then_event_sent_on_bus(self):
        expected_event = CreateLineEvent(self.line_serialized)

        self.notifier.created(self.line)

        self.bus.send_bus_event.assert_called_once_with(
            expected_event, headers=self.expected_headers
        )

    def test_when_line_edited_then_sip_reloaded(self):
        updated_fields = ['name']
        self.notifier.edited(self.line, updated_fields)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_when_line_edited_and_undefined_change_then_sip_reloaded(self):
        self.notifier.edited(self.line, None)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_when_line_edited_and_no_change_then_sip_not_reloaded(self):
        updated_fields = []
        self.notifier.edited(self.line, updated_fields)

        self.sysconfd.exec_request_handlers.assert_not_called()

    def test_when_line_edited_then_event_sent_on_bus(self):
        expected_event = EditLineEvent(self.line_serialized)

        self.notifier.edited(self.line, None)

        self.bus.send_bus_event.assert_called_once_with(
            expected_event, headers=self.expected_headers
        )

    def test_when_line_deleted_then_sip_reloaded(self):
        self.notifier.deleted(self.line)

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)

    def test_when_line_deleted_then_event_sent_on_bus(self):
        expected_event = DeleteLineEvent(self.line_serialized)

        self.notifier.deleted(self.line)

        self.bus.send_bus_event.assert_called_once_with(
            expected_event, headers=self.expected_headers
        )
