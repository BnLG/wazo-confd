# -*- coding: UTF-8 -*-
# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.resources.line_extension import dao as line_extension_dao

from .notifier import build_notifier
from .validator import build_validator


class LineExtensionService(object):

    def __init__(self, dao, notifier, validator):
        self.dao = dao
        self.notifier = notifier
        self.validator = validator

    def get(self, line, extension):
        self.dao.get_by(line_id=line.id, extension_id=extension.id)

    def find_all_by(self, **criteria):
        return self.dao.find_all_by(**criteria)

    def associate(self, line, extension):
        self.validator.validate_association(line, extension)
        line_extension = self.dao.associate(line, extension)
        self.notifier.associated(line, extension)
        return line_extension

    def dissociate(self, line, extension):
        self.validator.validate_dissociation(line, extension)
        self.dao.dissociate(line, extension)
        self.notifier.dissociated(line, extension)


def build_service():
    return LineExtensionService(line_extension_dao,
                                build_notifier(),
                                build_validator())
