# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.skill.event import (
    CreateSkillEvent,
    DeleteSkillEvent,
    EditSkillEvent,
)

from xivo_confd import bus


class SkillNotifier(object):

    def __init__(self, bus):
        self.bus = bus

    def created(self, skill):
        event = CreateSkillEvent(skill.id)
        self.bus.send_bus_event(event)

    def edited(self, skill):
        event = EditSkillEvent(skill.id)
        self.bus.send_bus_event(event)

    def deleted(self, skill):
        event = DeleteSkillEvent(skill.id)
        self.bus.send_bus_event(event)


def build_notifier():
    return SkillNotifier(bus)
