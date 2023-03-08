# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from unittest.mock import patch

from django.http import HttpResponse
from django.test.client import RequestFactory

from bedrock.mozorg.tests import TestCase
from bedrock.stories import views


@patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
class SwitchTests(TestCase):
    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="on")
    def test_stories_landing_contentful(self, render_mock):
        """Should use contentful landing template when switch is ON"""
        req = RequestFactory().get("/stories/")
        req.locale = "en-US"
        view = views.landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "stories/contentful-landing.html"

    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="on")
    def test_stories_article_contentful(self, render_mock):
        """Should use contentful story template when switch is ON"""
        req = RequestFactory().get("/stories/any-slug")
        req.locale = "en-US"
        slug = "any-slug"
        views.story_page(req, slug)
        template = render_mock.call_args[0][1]
        assert template == "stories/contentful-story.html"

    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="off")
    def test_stories_landing_static(self, render_mock):
        """Should use static landing template when switch is OFF"""
        req = RequestFactory().get("/stories/")
        req.locale = "en-US"
        view = views.landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "stories/landing.html"

    # test existing story article pages
    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="off")
    def test_stories_article_art_of_engagement(self, render_mock):
        """Should use static article template when switch is OFF"""
        req = RequestFactory().get("/stories/art-of-engagement")
        req.locale = "en-US"
        slug = "art-of-engagement"
        views.story_page(req, slug)
        template = render_mock.call_args[0][1]
        assert template == "stories/articles/art-of-engagement.html"

    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="off")
    def test_stories_article_build_together(self, render_mock):
        """Should use static article template when switch is OFF"""
        req = RequestFactory().get("/stories/build-together")
        req.locale = "en-US"
        slug = "build-together"
        views.story_page(req, slug)
        template = render_mock.call_args[0][1]
        assert template == "stories/articles/build-together.html"

    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="off")
    def test_stories_article_dreaming_then_building(self, render_mock):
        """Should use static article template when switch is OFF"""
        req = RequestFactory().get("/stories/community-champion")
        req.locale = "en-US"
        slug = "community-champion"
        views.story_page(req, slug)
        template = render_mock.call_args[0][1]
        assert template == "stories/articles/community-champion.html"

    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="off")
    def test_stories_article_(self, render_mock):
        """Should use static article template when switch is OFF"""
        req = RequestFactory().get("/stories/dreaming-then-building")
        req.locale = "en-US"
        slug = "dreaming-then-building"
        views.story_page(req, slug)
        template = render_mock.call_args[0][1]
        assert template == "stories/articles/dreaming-then-building.html"

    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="off")
    def test_stories_article_joy_of_color(self, render_mock):
        """Should use static article template when switch is OFF"""
        req = RequestFactory().get("/stories/joy-of-color")
        req.locale = "en-US"
        slug = "joy-of-color"
        views.story_page(req, slug)
        template = render_mock.call_args[0][1]
        assert template == "stories/articles/joy-of-color.html"

    @patch.dict(os.environ, SWITCH_CONTENTFUL_PRODUCT_STORY="off")
    def test_stories_article_raising_technology_eq(self, render_mock):
        """Should use static article template when switch is OFF"""
        req = RequestFactory().get("/stories/raising-technology-eq")
        req.locale = "en-US"
        slug = "raising-technology-eq"
        views.story_page(req, slug)
        template = render_mock.call_args[0][1]
        assert template == "stories/articles/raising-technology-eq.html"
