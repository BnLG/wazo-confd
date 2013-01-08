# -*- coding: UTF-8 -*-

# Copyright (C) 2012  Avencall
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


# -*- coding: UTF-8 -*-
#
# Copyright (C) 2012  Avencall
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

from xivo_recording.dao.recording_details_dao import RecordingDetailsDbBinder
from xivo_recording.services.manager_utils import _init_db_connection, \
    reconnectable
import logging
from xivo_dao.agentfeaturesdao import AgentFeaturesDAO

logger = logging.getLogger(__name__)


class RecordingManagement:

    def __init__(self):
        self.recording_details_db = _init_db_connection(RecordingDetailsDbBinder)
        #self.recording_details_db = RecordingDetailsDbBinder.new_from_uri(RecordingConfig.RECORDING_DB_URI)
        self.agentFeatDao = AgentFeaturesDAO(self.recording_details_db.session)

    @reconnectable("recording_details_db")
    def add_recording(self, campaign_id, params):
        """
        Converts data to the final format and calls the DAO
        """
        logger.debug("Add_recording")
        recording_details = {}
        for item in params:
            if (item == 'agent_no'):
                agent_id = self.agentFeatDao.agent_id(params['agent_no'])
                logger.debug("Replacing agent number: " + params['agent_no'] + " by agent id: " + agent_id)
                recording_details["agent_id"] = agent_id
            else:
                recording_details[item] = params[item]

        recording_details['campaign_id'] = str(campaign_id)
        result = self.recording_details_db.add_recording(recording_details)
        return result

    @reconnectable("recording_details_db")
    def get_recordings_as_dict(self, campaign_id, search=None):
        logger.debug("get_recordings_as_dict")

        search_pattern = {}
        for item in search:
            if (item == 'agent_no'):
                search_pattern["agent_id"] = self.agentFeatDao.agent_id(search['agent_no'])
            else:
                search_pattern[item] = search[item]

        result = self.recording_details_db. \
                            get_recordings_as_list(campaign_id, search_pattern)

        return result
