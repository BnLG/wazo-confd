# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from datetime import datetime
from mock import patch, Mock
from xivo_dao.alchemy.record_campaigns import RecordCampaigns
from xivo_restapi.rest.helpers import global_helper
import copy
import unittest


class TestCampaignsHelper(unittest.TestCase):

    def test_supplement_add_input(self):
        data = {"champ1": "valeur1",
                "champ2": "valeur2",
                "champ3": ""}
        old_data = copy.deepcopy(data)
        from xivo_restapi.rest.helpers import campaigns_helper
        result = campaigns_helper.supplement_add_input(data)
        old_data["champ3"] = None
        old_data["end_date"] = datetime.now().strftime("%Y-%m-%d")
        old_data["start_date"] = datetime.now().strftime("%Y-%m-%d")
        self.assertEquals(old_data, result)

    def test_supplement_edit_input(self):
        data = {"champ1": "valeur1",
                "champ2": "valeur2",
                "champ3": ""}
        old_data = copy.deepcopy(data)
        from xivo_restapi.rest.helpers import campaigns_helper
        result = campaigns_helper.supplement_edit_input(data)
        old_data["champ3"] = None
        self.assertTrue(old_data == result)

    @patch('xivo_restapi.rest.helpers.global_helper.create_class_instance')
    def test_create_instance(self, patch_create_class_instance):
        data = {'campaign_name': 'name'}
        mock_return_value = Mock()
        mock_return_value.start_date = '2012-12-12'
        mock_return_value.end_date = '2012-12-13'
        patch_create_class_instance.return_value = mock_return_value
        global_helper.str_to_datetime = Mock()
        from xivo_restapi.rest.helpers import campaigns_helper
        result = campaigns_helper.create_instance(data)
        global_helper.create_class_instance.assert_called_with(RecordCampaigns, data)
        self.assertEqual(result, mock_return_value)
