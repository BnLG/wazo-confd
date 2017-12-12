# -*- coding: utf-8 -*-
# Copyright 2016-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from mock import Mock

from xivo_bus.resources.group_member.event import GroupMemberUsersAssociatedEvent
from xivo_dao.alchemy.userfeatures import UserFeatures as User
from xivo_dao.alchemy.groupfeatures import GroupFeatures as Group

from ..notifier import GroupMemberNotifier


SYSCONFD_HANDLERS = {'ctibus': [],
                     'ipbx': ['sip reload',
                              'module reload app_queue.so',
                              'module reload chan_sccp.so'],
                     'agentbus': []}


class TestGroupMemberUserNotifier(unittest.TestCase):

    def setUp(self):
        self.bus = Mock()
        self.sysconfd = Mock()
        self.user1 = Mock(User, uuid='abcd-1234')
        self.user2 = Mock(User, uuid='efgh-5678')
        self.group = Mock(Group, id=3)

        self.notifier = GroupMemberNotifier(self.bus, self.sysconfd)

    def test_associate_then_bus_event(self):
        expected_event = GroupMemberUsersAssociatedEvent(self.group.id, [self.user1.uuid, self.user2.uuid])

        self.notifier.users_associated(self.group, [self.user1, self.user2])

        self.bus.send_bus_event.assert_called_once_with(expected_event)

    def test_associate_then_sysconfd_event(self):
        self.notifier.users_associated(self.group, [self.user1, self.user2])

        self.sysconfd.exec_request_handlers.assert_called_once_with(SYSCONFD_HANDLERS)
