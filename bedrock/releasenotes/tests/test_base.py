# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pathlib import Path

from django.core.cache import caches
from django.http import Http404, HttpResponse
from django.test.client import RequestFactory
from django.test.utils import override_settings

from mock import Mock, patch

from bedrock.base.urlresolvers import reverse
from bedrock.firefox.firefox_details import FirefoxDesktop
from bedrock.mozorg.tests import TestCase
from bedrock.releasenotes import views
from bedrock.releasenotes.models import ProductRelease

TESTS_PATH = Path(__file__).parent
DATA_PATH = str(TESTS_PATH.joinpath("data"))
RELEASES_PATH = str(TESTS_PATH)


@override_settings(RELEASE_NOTES_PATH=RELEASES_PATH)
class TestReleaseViews(TestCase):
    # Set DEV=False, otherwise all the releases will be erroneously made public
    # through the following refresh function, leading to wrong results in
    # get_release_or_404
    @override_settings(DEV=False)
    def setUp(self):
        ProductRelease.objects.refresh()
        caches["release-notes"].clear()
        self.activate("en-US")
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

        self.render_patch = patch("bedrock.releasenotes.views.l10n_utils.render")
        self.mock_render = self.render_patch.start()
        self.mock_render.return_value.has_header.return_value = False

    def tearDown(self):
        self.render_patch.stop()

    @property
    def last_ctx(self):
        """
        Convenient way to access the context of the last rendered
        response.
        """
        return self.mock_render.call_args[0][2]

    @patch("bedrock.releasenotes.models.get_release")
    def test_get_release_or_404(self, get_release):
        assert views.get_release_or_404("version", "product") == get_release.return_value
        get_release.assert_called_with("product", "version", None, False)
        get_release.return_value = None
        with self.assertRaises(Http404):
            views.get_release_or_404("version", "product")

    def test_get_release_or_404_esr(self):
        rel = views.get_release_or_404("24.5.0", "Firefox")
        assert rel.version == "24.5.0"
        assert rel.channel == "ESR"

    def test_get_release_or_404_endswith_esr(self):
        rel = views.get_release_or_404("45.0esr", "Firefox")
        assert rel.version == "45.0esr"
        assert rel.channel == "ESR"

    @override_settings(DEV=False)
    @patch("bedrock.releasenotes.views.release_notes_template")
    @patch("bedrock.releasenotes.views.get_release_or_404")
    @patch("bedrock.releasenotes.views.equivalent_release_url")
    def test_release_notes(self, mock_equiv_rel_url, get_release_or_404, mock_release_notes_template):
        """
        Should use release returned from get_release_or_404 with the
        correct params and pass the correct context variables and
        template to l10n_utils.render.
        """
        mock_release = get_release_or_404.return_value
        mock_release.major_version = "34"
        mock_release.notes.return_value = []

        views.release_notes(self.request, "27.0")
        get_release_or_404.assert_called_with("27.0", "Firefox", True)
        assert self.last_ctx["version"] == "27.0"
        assert self.last_ctx["release"] == mock_release
        assert self.mock_render.call_args[0][1] == mock_release_notes_template.return_value
        mock_equiv_rel_url.assert_called_with(mock_release)
        mock_release_notes_template.assert_called_with(mock_release.channel, "Firefox", 34)

    @patch("bedrock.releasenotes.views.get_release_or_404")
    def test_release_notes_beta_redirect(self, get_release_or_404):
        """
        Should redirect to url for beta release
        """
        release = Mock()
        release.get_absolute_url.return_value = "/firefox/27.0beta/releasenotes/"
        get_release_or_404.side_effect = [Http404, release]
        response = views.release_notes(self.request, "27.0")
        assert response.status_code == 302
        assert response["location"] == "/firefox/27.0beta/releasenotes/"
        get_release_or_404.assert_called_with("27.0beta", "Firefox", True)

    @patch("bedrock.releasenotes.views.get_release_or_404")
    def test_system_requirements(self, get_release_or_404):
        """
        Should use release returned from get_release_or_404, with a
        default channel of Release and default product of Firefox,
        and pass the version to l10n_utils.render
        """
        views.system_requirements(self.request, "27.0.1")
        get_release_or_404.assert_called_with("27.0.1", "Firefox")
        assert self.last_ctx["release"] == get_release_or_404.return_value
        assert self.last_ctx["version"] == "27.0.1"
        assert self.mock_render.call_args[0][1] == "firefox/releases/system_requirements.html"

    def test_release_notes_template(self):
        """
        Should return correct template name based on channel
        and product
        """
        assert views.release_notes_template("Nightly", "Firefox") == "firefox/releases/nightly-notes.html"
        assert views.release_notes_template("Aurora", "Firefox") == "firefox/releases/aurora-notes.html"
        assert views.release_notes_template("Aurora", "Firefox", 35) == "firefox/releases/dev-browser-notes.html"
        assert views.release_notes_template("Aurora", "Firefox", 34) == "firefox/releases/aurora-notes.html"
        assert views.release_notes_template("Beta", "Firefox") == "firefox/releases/beta-notes.html"
        assert views.release_notes_template("Release", "Firefox") == "firefox/releases/release-notes.html"
        assert views.release_notes_template("ESR", "Firefox") == "firefox/releases/esr-notes.html"
        assert views.release_notes_template("", "") == "firefox/releases/release-notes.html"

    @override_settings(DEV=False)
    def test_non_public_release(self):
        """
        Should raise 404 if release is not public and not settings.DEV, unless
        the include_drafts option is enabled
        """
        with self.assertRaises(Http404):
            views.get_release_or_404("58.0a1", "Firefox")
        assert not views.get_release_or_404("58.0a1", "Firefox", True).is_public
        with self.assertRaises(Http404):
            views.get_release_or_404("58.0a1", "Firefox for Android")
        assert not views.get_release_or_404("58.0a1", "Firefox for Android", True).is_public

    def test_no_equivalent_release_url(self):
        """
        Should return None
        """
        release = Mock()
        release.equivalent_android_release.return_value = None
        release.equivalent_desktop_release.return_value = None
        assert views.equivalent_release_url(release) is None

    def test_android_equivalent_release_url(self):
        """
        Should return the url for the equivalent android release
        """
        release = Mock()
        assert views.equivalent_release_url(release) == release.equivalent_android_release.return_value.get_absolute_url.return_value

    def test_desktop_equivalent_release_url(self):
        """
        Should return the url for the equivalent desktop release
        """
        release = Mock()
        release.equivalent_android_release.return_value = None
        assert views.equivalent_release_url(release) == release.equivalent_desktop_release.return_value.get_absolute_url.return_value

    def test_get_download_url_android(self):
        """
        Shoud return the download link for the release.channel from
        android_builds. Note that the channel names are from ship-it, so those
        are different from the internal names like release, beta or alpha.
        """
        store_url = "https://play.google.com/store/apps/details?id=%s"

        release = Mock(product="Firefox for Android", channel="Release")
        link = views.get_download_url(release)
        assert link.startswith(store_url % "org.mozilla.firefox")

        release = Mock(product="Firefox for Android", channel="Beta")
        link = views.get_download_url(release)
        assert link.startswith(store_url % "org.mozilla.firefox_beta")

        release = Mock(product="Firefox for Android", channel="Nightly")
        link = views.get_download_url(release)
        assert link.startswith(store_url % "org.mozilla.fenix")

    def test_check_url(self):
        with self.activate("en-US"):
            assert views.check_url("Firefox for Android", "45.0") == "https://support.mozilla.org/kb/will-firefox-work-my-mobile-device"
            assert views.check_url("Firefox for Android", "46.0") == "/en-US/firefox/android/46.0/system-requirements/"
            assert views.check_url("Firefox for iOS", "1.4") == "/en-US/firefox/ios/1.4/system-requirements/"
            assert views.check_url("Firefox", "42.0") == "/en-US/firefox/42.0/system-requirements/"

    @override_settings(DEV=False)
    def test_nightly_feed(self):
        """Nightly Notes feed should be served with public changes"""
        views.nightly_feed(self.request)
        assert len(self.last_ctx["notes"]) == 24
        assert self.last_ctx["notes"][0].id == 787237
        assert self.last_ctx["notes"][1].id == 787246
        assert self.last_ctx["notes"][2].id == 787245
        assert self.last_ctx["notes"][3].id == 787115
        assert self.last_ctx["notes"][4].id == 787108

    @override_settings(DEV=True)
    def test_nightly_feed_dev_mode(self):
        """Nightly Notes feed should be served with all changes in DEV"""
        views.nightly_feed(self.request)
        assert len(self.last_ctx["notes"]) == 26


class TestReleaseNotesIndex(TestCase):
    pd_cache = caches["product-details"]

    def setUp(self):
        self.pd_cache.clear()

    @patch("bedrock.releasenotes.views.l10n_utils.render")
    def test_relnotes_index_firefox(self, render_mock):
        firefox_desktop = FirefoxDesktop(json_dir=DATA_PATH)
        with patch("bedrock.releasenotes.views.firefox_desktop", firefox_desktop):
            render_mock().render.return_value = HttpResponse("")
            with self.activate("en-US"):
                self.client.get(reverse("firefox.releases.index"))
            releases = render_mock.call_args[0][2]["releases"]
            assert len(releases) == len(firefox_desktop.firefox_history_major_releases)
            assert releases[0][0] == 82.0
            assert releases[0][1]["major"] == "82.0"
            assert releases[0][1]["minor"] == ["82.0.1", "82.0.2", "82.0.3"]
            assert releases[4][0] == 78.0
            assert releases[4][1]["major"] == "78.0"
            assert releases[4][1]["minor"] == ["78.0.1", "78.0.2", "78.1.0", "78.2.0", "78.3.0", "78.3.1", "78.4.0", "78.4.1"]
            assert releases[49][0] == 33.1
            assert releases[49][1]["major"] == "33.1"
            assert releases[49][1]["minor"] == ["33.1.1"]
            assert releases[50][0] == 33.0
            assert releases[50][1]["major"] == "33.0"
            assert releases[50][1]["minor"] == ["33.0.1", "33.0.2", "33.0.3"]
            assert releases[52][0] == 31.0
            assert releases[52][1]["major"] == "31.0"
            assert releases[52][1]["minor"] == [
                "31.1.0",
                "31.1.1",
                "31.2.0",
                "31.3.0",
                "31.4.0",
                "31.5.0",
                "31.5.2",
                "31.5.3",
                "31.6.0",
                "31.7.0",
                "31.8.0",
            ]
            assert releases[69][1]["major"] == "14.0.1"
            assert releases[69][1]["minor"] == []
            # ensure v5.0 doesn't match v50.0
            assert releases[78][1]["major"] == "5.0"
            assert releases[78][1]["minor"] == ["5.0.1"]


class TestNotesRedirects(TestCase):
    def _test(self, url_from, url_to):
        with self.activate("en-US"):
            url = "/en-US" + url_from
        response = self.client.get(url)
        assert response.status_code == 302
        assert response["Location"] == "/en-US" + url_to

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox", version="22.0", channel="Release")),
    )
    def test_desktop_release_version(self):
        self._test("/firefox/notes/", "/firefox/22.0/releasenotes/")
        self._test("/firefox/latest/releasenotes/", "/firefox/22.0/releasenotes/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox", version="23.0beta", channel="Beta")),
    )
    def test_desktop_beta_version(self):
        self._test("/firefox/beta/notes/", "/firefox/23.0beta/releasenotes/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox", version="23.0beta", channel="Beta")),
    )
    def test_desktop_developer_version(self):
        self._test("/firefox/developer/notes/", "/firefox/23.0beta/releasenotes/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404", Mock(return_value=ProductRelease(product="Firefox", version="24.2.0", channel="ESR"))
    )
    def test_desktop_esr_version(self):
        self._test("/firefox/organizations/notes/", "/firefox/24.2.0/releasenotes/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox for Android", version="22.0", channel="Release")),
    )
    def test_android_release_version(self):
        self._test("/firefox/android/notes/", "/firefox/android/22.0/releasenotes/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox for Android", version="23.0beta", channel="Beta")),
    )
    def test_android_beta_version(self):
        self._test("/firefox/android/beta/notes/", "/firefox/android/23.0beta/releasenotes/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox for Android", version="24.0a2", channel="Aurora")),
    )
    def test_android_aurora_version(self):
        self._test("/firefox/android/aurora/notes/", "/firefox/android/24.0a2/auroranotes/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox for iOS", version="1.4", channel="Release")),
    )
    def test_ios_release_version(self):
        self._test("/firefox/ios/notes/", "/firefox/ios/1.4/releasenotes/")


class TestSysreqRedirect(TestCase):
    def _test(self, url_from, url_to):
        with self.activate("en-US"):
            url = "/en-US" + url_from
        response = self.client.get(url)
        assert response.status_code == 302
        assert response["Location"] == "/en-US" + url_to

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox", version="22.0", channel="Release")),
    )
    def test_desktop_release_version(self):
        self._test("/firefox/system-requirements/", "/firefox/22.0/system-requirements/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox", version="23.0beta", channel="Beta")),
    )
    def test_desktop_beta_version(self):
        self._test("/firefox/beta/system-requirements/", "/firefox/23.0beta/system-requirements/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404",
        Mock(return_value=ProductRelease(product="Firefox", version="23.0beta", channel="Beta")),
    )
    def test_desktop_developer_version(self):
        self._test("/firefox/developer/system-requirements/", "/firefox/23.0beta/system-requirements/")

    @patch(
        "bedrock.releasenotes.views.get_latest_release_or_404", Mock(return_value=ProductRelease(product="Firefox", version="24.2.0", channel="ESR"))
    )
    def test_desktop_esr_version(self):
        self._test("/firefox/organizations/system-requirements/", "/firefox/24.2.0/system-requirements/")
