# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from os.path import join

from django.http import Http404, HttpResponse
from django.test import RequestFactory

from mock import patch, ANY
from nose.tools import eq_

from bedrock.mozorg.tests import TestCase

from bedrock.legal_docs import views


class TestLoadLegalDoc(TestCase):
    @patch.object(views, 'listdir')
    def test_legal_doc_not_found(self, listdir_mock):
        listdir_mock.return_value = ['en-US.md']
        doc = views.load_legal_doc('the_dude_is_legal', 'de')
        self.assertIsNone(doc['content'])
        self.assertFalse(doc['localized'])
        self.assertDictEqual(doc['translations'], {'en-US': 'English (US)'})

    @patch.object(views, 'listdir')
    @patch.object(views, 'StringIO')
    @patch.object(views, 'md')
    def test_legal_doc_exists(self, md_mock, sio_mock, listdir_mock):
        """Should return the content of the en-US file if it exists."""
        sio_mock.StringIO.return_value.getvalue.return_value = "You're not wrong Walter..."
        listdir_mock.return_value = ['.mkdir', 'de.md', 'en-US.md']
        doc = views.load_legal_doc('the_dude_exists', 'de')
        good_path = join(views.LEGAL_DOCS_PATH, 'the_dude_exists', 'en-US.md')
        md_mock.markdownFromFile.assert_called_with(
            input=good_path, output=ANY, extensions=ANY)
        self.assertEqual(doc['content'], "You're not wrong Walter...")
        self.assertFalse(doc['localized'])
        self.assertDictEqual(doc['translations'], {'de': 'Deutsch', 'en-US': 'English (US)'})

    @patch('os.path.exists')
    @patch.object(views, 'listdir')
    @patch.object(views, 'StringIO')
    @patch.object(views, 'md')
    def test_localized_legal_doc_exists(self, md_mock, sio_mock, listdir_mock, exists_mock):
        sio_mock.StringIO.return_value.getvalue.return_value = "You're not wrong Walter..."
        exists_mock.return_value = True
        listdir_mock.return_value = ['.mkdir', 'de.md', 'en-US.md']
        doc = views.load_legal_doc('the_dude_exists', 'de')
        good_path = join(views.LEGAL_DOCS_PATH, 'the_dude_exists', 'de.md')
        md_mock.markdownFromFile.assert_called_with(
            input=good_path, output=ANY, extensions=ANY)
        self.assertEqual(doc['content'], "You're not wrong Walter...")
        self.assertTrue(doc['localized'])
        self.assertDictEqual(doc['translations'], {'de': 'Deutsch', 'en-US': 'English (US)'})


class TestLegalDocView(TestCase):
    @patch.object(views, 'load_legal_doc')
    def test_missing_doc_is_404(self, lld_mock):
        lld_mock.return_value = None
        req = RequestFactory().get('/dude/is/gone/')
        req.locale = 'de'
        view = views.LegalDocView.as_view(template_name='base.html',
                                          legal_doc_name='the_dude_is_gone')
        with self.assertRaises(Http404):
            view(req)

        lld_mock.assert_called_with('the_dude_is_gone', 'de')

    @patch.object(views, 'load_legal_doc')
    @patch.object(views.l10n_utils, 'render')
    def test_good_doc_okay(self, render_mock, lld_mock):
        """Should render correct thing when all is well"""
        doc_value = "Donny, you're out of your element!"
        lld_mock.return_value = {
            'content': doc_value,
            'localized': True,
            'translations': {'de': 'Deutsch', 'en-US': 'English (US)'},
        }
        good_resp = HttpResponse(doc_value)
        render_mock.return_value = good_resp
        req = RequestFactory().get('/dude/exists/')
        req.locale = 'de'
        view = views.LegalDocView.as_view(template_name='base.html',
                                          legal_doc_name='the_dude_exists')
        resp = view(req)
        eq_(resp['cache-control'], 'max-age={0!s}'.format(views.CACHE_TIMEOUT))
        eq_(resp.content, doc_value)
        eq_(render_mock.call_args[0][2]['doc'], doc_value)
        self.assertTrue(render_mock.call_args[0][2]['localized'])
        lld_mock.assert_called_with('the_dude_exists', 'de')

    @patch.object(views, 'load_legal_doc')
    @patch.object(views.l10n_utils, 'render')
    def test_cache_settings(self, render_mock, lld_mock):
        """Should use the cache_timeout value from view."""
        doc_value = "Donny, you're out of your element!"
        lld_mock.return_value = {
            'content': doc_value,
            'localized': True,
            'translations': {'es-ES': 'Espa\u00f1ol (de Espa\u00f1a)', 'en-US': 'English (US)'},
        }
        good_resp = HttpResponse(doc_value)
        render_mock.return_value = good_resp
        req = RequestFactory().get('/dude/exists/cached/')
        req.locale = 'es-ES'
        view = views.LegalDocView.as_view(template_name='base.html',
                                          legal_doc_name='the_dude_exists',
                                          cache_timeout=10)
        resp = view(req)
        eq_(resp['cache-control'], 'max-age=10')

    @patch.object(views, 'load_legal_doc')
    @patch.object(views.l10n_utils, 'render')
    def test_cache_class_attrs(self, render_mock, lld_mock):
        """Should use the cache_timeout value from view class."""
        doc_value = "Donny, you're out of your element!"
        lld_mock.return_value = {
            'content': doc_value,
            'localized': True,
            'translations': {'es-ES': 'Espa\u00f1ol (de Espa\u00f1a)', 'en-US': 'English (US)'},
        }
        good_resp = HttpResponse(doc_value)
        render_mock.return_value = good_resp
        req = RequestFactory().get('/dude/exists/cached/2/')
        req.locale = 'es-ES'

        class DocTestView(views.LegalDocView):
            cache_timeout = 20
            template_name = 'base.html'
            legal_doc_name = 'the_dude_abides'

        view = DocTestView.as_view()
        resp = view(req)
        eq_(resp['cache-control'], 'max-age=20')
        lld_mock.assert_called_with('the_dude_abides', 'es-ES')
