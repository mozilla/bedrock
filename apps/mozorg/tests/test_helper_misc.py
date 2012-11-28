import unittest

from django.conf import settings
from django.test.client import Client

import basket
import jingo
from mock import patch
from nose.tools import assert_false, eq_, ok_
from pyquery import PyQuery as pq


# Where should this function go?
def render(s, context={}):
    t = jingo.env.from_string(s)
    return t.render(**context)


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

    @patch.object(basket, 'subscribe')
    def test_post_correct_form(self, sub_mock):
        data = {
            'newsletter-footer': 'Y',
            'newsletter': 'mozilla-and-you',
            'email': 'foo@bar.com',
            'country': 'us',
            'lang': 'en',
            'fmt': 'H',
            'privacy': 'Y',
            'source_url': 'http://allizom.com/en-US/base/',
        }
        response = self.client.post('/en-US/base/', data)
        doc = pq(response.content)
        assert_false(doc('form#footer-email-form'))
        ok_(doc('div#footer-email-form.thank'))
        sub_mock.assert_called_with('foo@bar.com', 'mozilla-and-you',
                                    format='H', country='us', lang='en',
                                    source_url='http://allizom.com/en-US/base/')

    @patch.object(basket, 'subscribe')
    def test_post_form_country_lang_not_required(self, sub_mock):
        """
        Form should successfully post without country, lang, or src url.
        """
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
        sub_mock.assert_called_with('foo@bar.com', 'mozilla-and-you',
                                    format='H')

    def test_post_wrong_form(self):
        response = self.client.post('/en-US/base/', {'newsletter-footer': 'Y'})
        doc = pq(response.content)
        ok_(doc('#footer-email-errors'))
        ok_(doc('#footer-email-form.has-errors'))
