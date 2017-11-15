# -*- coding: UTF-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from .notifier import build_notifier
from .validator import build_validator


class OutcallScheduleService(object):

    def __init__(self, notifier, validator):
        self.validator = validator
        self.notifier = notifier

    def associate(self, outcall, schedule):
        self.validator.validate_association(outcall, schedule)
        outcall.schedules = [schedule]
        self.notifier.associated(outcall, schedule)

    def dissociate(self, outcall, schedule):
        self.validator.validate_dissociation(outcall, schedule)
        outcall.schedules = []
        self.notifier.dissociated(outcall, schedule)


def build_service():
    return OutcallScheduleService(build_notifier(),
                                  build_validator())
