# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.utils import timezone

from pytz import utc

from bedrock import externalfiles
from bedrock.externalfiles.models import ExternalFile as EFModel
from bedrock.mozorg.tests import TestCase


class TestExternalFile(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestExternalFile, cls).setUpClass()
        timezone.activate(utc)

    def setUp(self):
        settings.EXTERNAL_FILES['test'] = {
            'url': 'http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul',
            'name': 'there.is.no.data.xul'
        }

    def tearDown(self):
        externalfiles.ExternalFile('test').clear_cache()
        del settings.EXTERNAL_FILES['test']

    def test_last_modified(self):
        """Should return the modified timestamp."""
        EFModel.objects.create(name='test', content='test')
        efo = EFModel.objects.get(name='test')
        self.assertEqual(externalfiles.ExternalFile('test').last_modified, efo.last_modified)
