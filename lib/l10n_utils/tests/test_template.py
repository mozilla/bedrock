# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pathlib import Path

from django.template import TemplateDoesNotExist
from django.test import RequestFactory

from django_jinja.backend import Jinja2
from mock import ANY, Mock, patch

from bedrock.mozorg.tests import TestCase
from lib.l10n_utils import render

ROOT_PATH = Path(__file__).with_name("test_files")
ROOT = str(ROOT_PATH)
TEMPLATE_DIRS = [str(ROOT_PATH.joinpath("templates"))]
jinja_env = Jinja2.get_default().env


class TestNoLocale(TestCase):
    @patch("lib.l10n_utils.django_render")
    def test_render_no_locale(self, django_render):
        # Our render method doesn't blow up if the request has no .locale
        # (can happen on 500 error path, for example)
        request = Mock(spec=object)
        request.path_info = "/some/path/"
        # Note: no .locale on request
        # Should not cause an exception
        render(request, "500.html")


@patch.object(jinja_env.loader, "searchpath", TEMPLATE_DIRS)
@patch("lib.l10n_utils.django_render")
class TestLocaleTemplates(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_enUS_render(self, django_render):
        """
        en-US requests without l10n or locale template should render the
        originally requested template.
        """
        django_render.side_effect = [TemplateDoesNotExist(""), True]
        request = self.rf.get("/")
        request.locale = "en-US"
        render(request, "firefox/new.html", {"active_locales": ["en-US"]})
        django_render.assert_called_with(request, "firefox/new.html", ANY)

    def test_bedrock_enUS_render(self, django_render):
        """
        en-US requests with a locale-specific template should render the
        locale-specific template.
        """
        django_render.side_effect = [True]
        request = self.rf.get("/")
        request.locale = "en-US"
        render(request, "firefox/new.html", {"active_locales": ["en-US"]})
        django_render.assert_called_with(request, "firefox/new.en-US.html", ANY)

    def test_default_render(self, django_render):
        """
        Non en-US requests without l10n or locale template should render the
        originally requested template.
        """
        django_render.side_effect = [TemplateDoesNotExist(""), True]
        request = self.rf.get("/")
        request.locale = "de"
        render(request, "firefox/new.html", {"active_locales": ["de"]})
        django_render.assert_called_with(request, "firefox/new.html", ANY)

    def test_bedrock_locale_render(self, django_render):
        """
        Non en-US requests with a locale-specific template should render the
        locale-specific template.
        """
        django_render.side_effect = [True]
        request = self.rf.get("/")
        request.locale = "es-ES"
        render(request, "firefox/new.html", {"active_locales": ["es-ES"]})
        django_render.assert_called_with(request, "firefox/new.es-ES.html", ANY)
