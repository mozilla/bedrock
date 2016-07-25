from django.test import TestCase, RequestFactory

import jingo
import jinja2
from nose.tools import eq_

from lib.l10n_utils import translation


class TestContext(TestCase):

    def setUp(self):
        translation.activate('en-US')
        self.factory = RequestFactory()

    def render(self, content, request=None):
        if not request:
            request = self.factory.get('/')
        tpl = jinja2.Template(content)
        return jingo.render_to_string(request, tpl)

    def test_request(self):
        eq_(self.render('{{ request.path }}'), '/')

    def test_settings(self):
        eq_(self.render('{{ settings.LANGUAGE_CODE }}'), 'en-US')

    def test_languages(self):
        eq_(self.render("{{ LANGUAGES['en-us'] }}"), 'English (US)')

    def test_lang_setting(self):
        eq_(self.render("{{ LANG }}"), 'en-US')

    def test_lang_dir(self):
        eq_(self.render("{{ DIR }}"), 'ltr')
