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

from xivo_dao import queue_features_dao
from xivo_recording.dao.exceptions import DataRetrieveError
from xivo_recording.dao.record_campaign_dao import RecordCampaignDbBinder
from xivo_recording.services.manager_utils import _init_db_connection, \
    reconnectable
import logging

logger = logging.getLogger(__name__)


class CampagneManagement:

    def __init__(self):
        self.record_db = _init_db_connection(RecordCampaignDbBinder)
    
    @reconnectable("record_db")
    def create_campaign(self, params):
        result = self.record_db.add(params)
        return result

    def get_campaigns_as_dict(self, search=None, checkCurrentlyRunning = False):
        """
        Calls the DAO and converts data to the final format
        """
        result = self._get_campaigns_as_dict(search, checkCurrentlyRunning)

        try:
            for item in result:
                item["queue_name"] = queue_features_dao. \
                                        queue_name(item["queue_id"])
        except Exception as e:
            logger.critical("DAO failure(" + str(e) + ")!")
            raise DataRetrieveError("DAO failure(" + str(e) + ")!")

        return result
    
    @reconnectable("record_db")
    def _get_campaigns_as_dict(self, search=None, checkCurrentlyRunning = False):
        logger.debug("get_campaigns_as_dict")
        result = self.record_db.get_records_as_dict(search, checkCurrentlyRunning)
        return result
    
    @reconnectable("record_db")
    def update_campaign(self, campaign_id, params):
        logger.debug('going to update')
        result = self.record_db.update(campaign_id, params)
        return result
        