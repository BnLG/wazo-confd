# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..

import logging


logger = logging.getLogger(__name__)


def register_resources(core_rest_api, resources):
    for resource in resources:
        pkg_resource = 'xivo_confd.resources.{resource}'.format(resource=resource)
        _load_module('%s.actions' % pkg_resource, core_rest_api)


def _load_module(name, core_rest_api):
    try:
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
    except ImportError as e:
        logger.error('Module not found %s', name)
        logger.exception(e)
    else:
        mod.load(core_rest_api)
        logger.debug('Module successfully loaded: %s', name)
