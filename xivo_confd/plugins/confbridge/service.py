# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_dao.resources.asterisk_file import dao as asterisk_file_dao

from xivo_confd.helpers.asterisk import AsteriskConfigurationService

from .notifier import build_notifier


class ConfBridgeConfigurationService(AsteriskConfigurationService):

    file_name = 'confbridge.conf'


def build_service():
    return ConfBridgeConfigurationService(asterisk_file_dao,
                                          build_notifier())
