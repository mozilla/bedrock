# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pathlib import Path
from unittest.mock import ANY, patch

from django.template import TemplateDoesNotExist
from django.test import RequestFactory, override_settings

from django_jinja.backend import Jinja2

from bedrock.mozorg.tests import TestCase
from lib.l10n_utils import render, render_to_string

ROOT_PATH = Path(__file__).with_name("test_files")
ROOT = str(ROOT_PATH)
TEMPLATE_DIRS = [str(ROOT_PATH.joinpath("templates"))]
L10N_PATH = ROOT_PATH.joinpath("l10n")
jinja_env = Jinja2.get_default().env


class TestNoLocale(TestCase):
    @patch("lib.l10n_utils.django_render")
    def test_render_no_locale(self, django_render):
        request = RequestFactory().get("/invalid/path/")
        # Note: no `locale` on request should not cause an exception.
        render(request, "500.html")


@override_settings(FLUENT_PATHS=[L10N_PATH])
@patch.object(jinja_env.loader, "searchpath", TEMPLATE_DIRS)
class TestFtlTemplateHelper(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_english_locale(self):
        req = self.rf.get("/en-US/")
        req.locale = "de"
        result = render_to_string("test-en-title.html", request=req, ftl_files="mozorg/fluent")
        assert result.strip() == "Title in German:This is a test of the new Fluent L10n system"

    def test_french_locale(self):
        req = self.rf.get("/en-US/")
        req.locale = "en-US"
        result = render_to_string("test-fr-title.html", request=req, ftl_files="mozorg/fluent")
        assert result.strip() == "This is a test of the new Fluent L10n system:Title in French"


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
        request = self.rf.get("/en-US/")
        request.locale = "en-US"
        render(request, "firefox/new.html", {"active_locales": ["en-US"]})
        django_render.assert_called_with(request, "firefox/new.html", ANY)

    def test_bedrock_enUS_render(self, django_render):
        """
        en-US requests with a locale-specific template should render the
        locale-specific template.
        """
        django_render.side_effect = [True]
        request = self.rf.get("/en-US/")
        request.locale = "en-US"
        render(request, "firefox/new.html", {"active_locales": ["en-US"]})
        django_render.assert_called_with(request, "firefox/new.en-US.html", ANY)

    def test_default_render(self, django_render):
        """
        Non en-US requests without l10n or locale template should render the
        originally requested template.
        """
        django_render.side_effect = [TemplateDoesNotExist(""), True]
        request = self.rf.get("/de/")
        request.locale = "de"
        render(request, "firefox/new.html", {"active_locales": ["de"]})
        django_render.assert_called_with(request, "firefox/new.html", ANY)

    def test_bedrock_locale_render(self, django_render):
        """
        Non en-US requests with a locale-specific template should render the
        locale-specific template.
        """
        django_render.side_effect = [True]
        request = self.rf.get("/es-ES/")
        request.locale = "es-ES"
        render(request, "firefox/new.html", {"active_locales": ["es-ES"]})
        django_render.assert_called_with(request, "firefox/new.es-ES.html", ANY)
