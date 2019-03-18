from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory

import jinja2

from lib.l10n_utils import translation


class TestContext(TestCase):

    def setUp(self):
        translation.activate('en-US')
        self.factory = RequestFactory()
        translation.activate('en-US')

    def render(self, content, request=None):
        if not request:
            request = self.factory.get('/')
        tpl = jinja2.Template(content)
        return render_to_string(tpl, request=request)

    def test_request(self):
        assert self.render('{{ request.path }}') == '/'

    def test_settings(self):
        assert self.render('{{ settings.LANGUAGE_CODE }}') == 'en-US'

    def test_languages(self):
        assert self.render("{{ LANGUAGES['en-us'] }}") == 'English (US)'

    def test_lang_setting(self):
        assert self.render("{{ LANG }}") == 'en-US'

    def test_lang_dir(self):
        assert self.render("{{ DIR }}") == 'ltr'
