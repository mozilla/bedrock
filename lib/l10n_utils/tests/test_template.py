# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.core.urlresolvers import clear_url_caches
from django.test.client import Client

from jingo import env
from jinja2 import FileSystemLoader
from mock import patch
from nose.plugins.skip import SkipTest
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from mozorg.tests import TestCase


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'),)


@patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
@patch.object(settings, 'ROOT_URLCONF', 'l10n_utils.tests.test_files.urls')
@patch.object(settings, 'ROOT', ROOT)
class TestTransBlocks(TestCase):
    def setUp(self):
        clear_url_caches()
        self.client = Client()

    def test_trans_block_works(self):
        """ Sanity check to make sure translations work at all. """
        response = self.client.get('/de/trans-block-reload-test/')
        doc = pq(response.content)
        gettext_call = doc('h1')
        trans_block = doc('p')
        eq_(gettext_call.text(), 'Die Lage von Mozilla')
        ok_(trans_block.text().startswith('Mozillas Vision des Internets ist'))

    def test_trans_block_works_reload(self):
        """
        Translation should work after a reload.

        bug 808580
        """
        self.test_trans_block_works()
        self.test_trans_block_works()


class TestTemplateLangFiles(TestCase):
    @patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
    def test_added_lang_files(self):
        """
        Lang files specified in the template should be added to the defaults.
        """
        template = env.get_template('some_lang_files.html')
        # make a dummy object capable of having arbitrary attrs assigned
        request = type('request', (), {})()
        template.render(request=request)
        eq_(request.langfiles, ['dude', 'walter',
                                'main', 'base', 'newsletter'])

    @patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
    def test_added_lang_files_inheritance(self):
        """
        Lang files specified in the template should be added to the defaults
        and any specified in parent templates.
        """
        raise SkipTest
        # TODO fix this. it is broken. hence the skip.
        #      does not pick up the files from the parent.
        #      captured in bug 797984.
        template = env.get_template('even_more_lang_files.html')
        # make a dummy object capable of having arbitrary attrs assigned
        request = type('request', (), {})()
        template.render(request=request)
        eq_(request.langfiles, ['donnie', 'smokey', 'jesus', 'dude', 'walter',
                                'main', 'base', 'newsletter'])
