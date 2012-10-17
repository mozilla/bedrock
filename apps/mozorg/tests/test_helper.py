import unittest

from django.conf import settings
from django.test.client import Client
from test_utils import RequestFactory

import basket
import jingo
from mock import Mock, patch
from nose.tools import assert_false, assert_not_equal, eq_, ok_
from product_details import product_details
from pyquery import PyQuery as pq


# Where should this function go?
def render(s, context={}):
    t = jingo.env.from_string(s)
    return t.render(**context)


class TestDownloadButtons(unittest.TestCase):

    def latest_version(self):
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def check_desktop_links(self, links):
        """Desktop links should have the correct firefox version"""
        key = 'firefox-%s' % self.latest_version()

        for link in links:
            assert_not_equal(pq(link).attr('href').find(key), -1)

    def check_dumb_button(self, doc):
        # Make sure 4 links are present
        links = doc('li a')
        eq_(links.length, 4)

        self.check_desktop_links(links[:3])

        # Check that last link is Android
        eq_(pq(links[3]).attr('href'),
            'https://market.android.com/details?id=org.mozilla.firefox')

    def test_button(self, format='large'):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', '%s') }}" % format,
                        {'request': get_request}))

        eq_(doc.attr('id'), 'button')

        self.check_dumb_button(doc('noscript'))
        self.check_dumb_button(doc('.unsupported-download'))
        self.check_dumb_button(doc('.download-list'))

        eq_(doc('.download-other a').length, 3)

    def test_small_button(self):
        self.test_button('small')

    def test_button_force_direct(self):
        """
        If the force_direct parameter is True, all download links must be
        directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', force_direct=true) }}",
                        {'request': get_request}))

        # Check that the first 3 links are direct.
        links = doc('.download-list a')
        for link in links[:3]:
            link = pq(link)
            ok_(link.attr('href')
                .startswith('https://download.mozilla.org'))
            # direct links should not have the data attr.
            ok_(link.attr('data-direct-link') is None)

    def test_button_has_data_attr_if_not_direct(self):
        """
        If the button points to the thank you page, it should have a
        `data-direct-link` attribute that contains the direct url.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button') }}",
                        {'request': get_request}))

        # The first 3 links should be for desktop.
        links = doc('.download-list a')
        for link in links[:3]:
            ok_(pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))
        # The fourth link is mobile and should not have the attr
        ok_(pq(links[3]).attr('data-direct-link') is None)

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_enabled_en_us(self):
        """Check that only the windows link goes to stub with en-US"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        ok_('stub' in pq(links[0]).attr('href'))
        for link in links[1:]:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_enabled_locales(self):
        """Check that the stub is not served to locales"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', False)
    def test_stub_aurora_installer_disabled_en_us(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('li a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', False)
    def test_stub_aurora_installer_disabled_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_override_en_us(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_button('button', build='aurora', \
                            force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_override_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', build='aurora', \
                            force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))


class TestVideoTag(unittest.TestCase):
    # Video stubs
    moz_video = 'http://videos.mozilla.org/serv/flux/example.%s'
    nomoz_video = 'http://example.org/example.%s'

    def test_empty(self):
        # No video, no output.
        eq_(render('{{ video() }}'), '')

    def test_video(self):
        # A few common variations
        videos = [self.nomoz_video % ext for ext in ('ogv', 'mp4', 'webm')]
        doc = pq(render("{{ video%s }}" % str(tuple(videos))))

        # Tags generated?
        eq_(doc('video').length, 1)
        eq_(doc('video source').length, 3)

        # Extensions in the right order?
        for i, ext in enumerate(('webm', 'ogv', 'mp4')):
            ok_(doc('video source:eq(%s)' % i).attr('src').endswith(ext))

    def test_prefix(self):
        # Prefix should be applied to all videos.
        doc = pq(render("{{ video('meh.mp4', 'meh.ogv', "
                        "prefix='http://example.com/blah/') }}"))
        expected = ('http://example.com/blah/meh.ogv',
                    'http://example.com/blah/meh.mp4')

        eq_(doc('video source').length, 2)

        for i in xrange(2):
            eq_(doc('video source:eq(%s)' % i).attr('src'), expected[i])

    def test_fileformats(self):
        # URLs ending in strange extensions are ignored.
        videos = [self.nomoz_video % ext for ext in
                  ('ogv', 'exe', 'webm', 'txt')]
        videos.append('http://example.net/noextension')
        doc = pq(render("{{ video%s }}" % (str(tuple(videos)))))

        eq_(doc('video source').length, 2)

        for i, ext in enumerate(('webm', 'ogv')):
            ok_(doc('video source:eq(%s)' % i).attr('src').endswith(ext))

    def test_flash_fallback(self):
        # Fallback by default for Mozilla-esque videos
        videos = [self.moz_video % ext for ext in ('ogv', 'mp4', 'webm')]
        doc = pq(render("{{ video%s }}" % str(tuple(videos))))

        eq_(doc('video object').length, 1)
        eq_(doc('object').attr('data'), doc('object param[name=movie]').val())

        # No fallback without mp4 file
        videos = [self.moz_video % ext for ext in ('ogv', 'webm')]
        doc = pq(render("{{ video%s }}" % str(tuple(videos))))

        eq_(doc('video object').length, 0)

        # No fallback without Mozilla CDN prefix
        videos = [self.nomoz_video % ext for ext in ('ogv', 'mp4', 'webm')]
        doc = pq(render("{{ video%s }}" % str(tuple(videos))))

        eq_(doc('video object').length, 0)


@patch.object(settings, 'ROOT_URLCONF', 'mozorg.tests.urls')
class TestNewsletterFunction(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_form(self):
        response = self.client.get('/en-US/base/')
        doc = pq(response.content)
        assert_false(doc('#footer-email-errors'))
        ok_(doc('form#footer-email-form'))

    @patch.object(basket, 'subscribe', Mock())
    def test_post_correct_form(self):
        data = {
            'newsletter-footer': 'Y',
            'newsletter': 'mozilla-and-you',
            'email': 'foo@bar.com',
            'fmt': 'H',
            'privacy': 'Y',
        }
        response = self.client.post('/en-US/base/', data)
        doc = pq(response.content)
        assert_false(doc('form#footer-email-form'))
        ok_(doc('div#footer-email-form.thank'))

    def test_post_wrong_form(self):
        response = self.client.post('/en-US/base/', {'newsletter-footer': 'Y'})
        doc = pq(response.content)
        ok_(doc('#footer-email-errors'))
        ok_(doc('#footer-email-form.has-errors'))
