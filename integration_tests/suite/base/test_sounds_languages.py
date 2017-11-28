# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, contains_inanyorder, equal_to
from . import confd, ari


def test_get():
    sounds = [
        {'id': 'conf-now-unmuted',
         'formats': [{'language': 'fr_CA',
                      'format': 'slin'},
                     {'language': 'en_US',
                      'format': 'slin'},
                     {'language': 'en',
                      'format': 'gsm'}],
         'text': 'The conference is now unmuted.'},
        {'id': 'queue-minutes',
         'formats': [{'language': 'fr_CA',
                      'format': 'slin'},
                     {'language': 'en_US',
                      'format': 'slin'},
                     {'language': 'en',
                      'format': 'gsm'},
                     {'language': 'fr_FR',
                      'format': 'slin'}],
         'text': 'minutes'}
    ]
    ari.set_sounds(sounds)

    response = confd.sounds.languages.get()
    response.assert_ok()

    assert_that(response.items, contains_inanyorder(
        {'tag': 'en_US'},
        {'tag': 'en'},
        {'tag': 'fr_CA'},
        {'tag': 'fr_FR'},
    ))
    assert_that(response.total, equal_to(4))
