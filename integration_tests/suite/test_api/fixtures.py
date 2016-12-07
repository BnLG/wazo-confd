# -*- coding: UTF-8 -*-

# Copyright (C) 2016 The Wazo Authors  (see the AUTHORS file)
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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from wrappers import IsolatedAction

import helpers as h


class user(IsolatedAction):

    actions = {'generate': h.user.generate_user,
               'delete': h.user.delete_user}


class line(IsolatedAction):

    actions = {'generate': h.line.generate_line,
               'delete': h.line.delete_line}


class line_sip(IsolatedAction):

    actions = {'generate': h.line_sip.generate_line,
               'delete': h.line_sip.delete_line}


class sip(IsolatedAction):

    actions = {'generate': h.endpoint_sip.generate_sip,
               'delete': h.endpoint_sip.delete_sip}


class sccp(IsolatedAction):

    actions = {'generate': h.endpoint_sccp.generate_sccp,
               'delete': h.endpoint_sccp.delete_sccp}


class extension(IsolatedAction):

    actions = {'generate': h.extension.generate_extension,
               'delete': h.extension.delete_extension}


class device(IsolatedAction):

    actions = {'generate': h.device.generate_device,
               'delete': h.device.delete_device}


class autoprov(IsolatedAction):

    actions = {'generate': h.device.generate_autoprov,
               'delete': h.device.delete_device}


class voicemail(IsolatedAction):

    actions = {'generate': h.voicemail.generate_voicemail,
               'delete': h.voicemail.delete_voicemail}


class context(IsolatedAction):

    actions = {'generate': h.context.generate_context,
               'delete': h.context.delete_context}


class csv_entry(IsolatedAction):

    actions = {'generate': h.user_import.generate_entry}


class custom(IsolatedAction):

    actions = {'generate': h.endpoint_custom.generate_custom,
               'delete': h.endpoint_custom.delete_custom}


class registrar(IsolatedAction):

    actions = {'generate': h.device.generate_registrar,
               'delete': h.device.delete_registrar}


class call_permission(IsolatedAction):

    actions = {'generate': h.call_permission.generate_call_permission,
               'delete': h.call_permission.delete_call_permission}


class entity(IsolatedAction):

    actions = {'generate': h.entity.generate_entity,
               'delete': h.entity.delete_entity}


class agent(IsolatedAction):

    actions = {'generate': h.agent.generate_agent,
               'delete': h.agent.delete_agent}


class funckey_template(IsolatedAction):

    actions = {'generate': h.funckey_template.generate_funckey_template,
               'delete': h.funckey_template.delete_funckey_template}


class call_pickup(IsolatedAction):

    actions = {'generate': h.call_pickup.generate_call_pickup,
               'delete': h.call_pickup.delete_call_pickup}


class call_filter(IsolatedAction):

    actions = {'generate': h.call_filter.generate_call_filter,
               'delete': h.call_filter.delete_call_filter}


class schedule(IsolatedAction):

    actions = {'generate': h.schedule.generate_schedule,
               'delete': h.schedule.delete_schedule}


class call_log(IsolatedAction):

    actions = {'generate': h.call_log.generate_call_log,
               'delete': h.call_log.delete_call_log}


class cti_profile(IsolatedAction):

    actions = {'generate': h.cti_profile.generate_cti_profile,
               'delete': h.cti_profile.delete_cti_profile}


class queue(IsolatedAction):

    actions = {'generate': h.queue.generate_queue,
               'delete': h.queue.delete_queue}


class trunk(IsolatedAction):

    actions = {'generate': h.trunk.generate_trunk,
               'delete': h.trunk.delete_trunk}


class incall(IsolatedAction):

    actions = {'generate': h.incall.generate_incall,
               'delete': h.incall.delete_incall}


class meetme(IsolatedAction):

    actions = {'generate': h.meetme.generate_conference,
               'delete': h.meetme.delete_conference}


class group(IsolatedAction):

    actions = {'generate': h.group.generate_group,
               'delete': h.group.delete_group}


class outcall(IsolatedAction):

    actions = {'generate': h.outcall.generate_outcall,
               'delete': h.outcall.delete_outcall}


class ivr(IsolatedAction):

    actions = {'generate': h.ivr.generate_ivr,
               'delete': h.ivr.delete_ivr}


class agent_login_status(IsolatedAction):

    actions = {'generate': h.agent_login_status.generate_agent_login_status,
               'delete': h.agent_login_status.delete_agent_login_status}


class conference(IsolatedAction):

    actions = {'generate': h.conference.generate_conference,
               'delete': h.conference.delete_conference}
