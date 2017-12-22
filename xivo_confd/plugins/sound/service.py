# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from .model import SoundCategory
from .notifier import build_notifier
from .schema import ASTERISK_CATEGORY
from .storage import build_storage
from .validator import build_validator, build_validator_file


class SoundService(object):

    def __init__(self, storage, validator, validator_file, notifier):
        self._storage = storage
        self.validator = validator
        self.validator_file = validator_file
        self.notifier = notifier

    def search(self, parameters):
        # XXX get Asterisk sounds
        sounds = self._storage.list_directories()
        # XXX merge Asterisk sounds
        total = len(sounds)
        return total, sounds

    def get(self, sound_name):
        if sound_name == ASTERISK_CATEGORY:
            # XXX return Asterisk sounds
            sound = SoundCategory(name='system')
        else:
            sound = self._storage.get_directory(sound_name)
        return sound

    def create(self, sound):
        self._storage.create_directory(sound)
        self.notifier.created(sound)
        return sound

    def delete(self, sound):
        self.validator.validate_delete(sound)
        self._storage.remove_directory(sound)
        self.notifier.deleted(sound)

    def load_file(self, sound, filename):
        if sound.name == ASTERISK_CATEGORY:
            # XXX return Asterisk sound binary
            sound = object()
        else:
            sound = self._storage.load_file(sound, filename)
        return sound

    def save_file(self, sound, filename, content):
        self.validator_file.validate_edit(sound)
        self._storage.save_file(sound, filename, content)

    def delete_file(self, sound, filename):
        self.validator_file.validate_delete(sound)
        self._storage.remove_file(sound, filename)


def build_service():
    return SoundService(build_storage(),
                        build_validator(),
                        build_validator_file(),
                        build_notifier())
