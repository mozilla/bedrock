import os.path

from mock import patch

from django.conf import settings
from django.test.client import Client, RequestFactory

import basket
import jingo
from nose.tools import assert_false, eq_, ok_
from pyquery import PyQuery as pq
from bedrock.newsletter.tests.test_views import newsletters
from funfactory.urlresolvers import reverse

from bedrock.mozorg.tests import TestCase


TEST_FILES_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'test_files')
TEST_L10N_IMG_PATH = os.path.join(TEST_FILES_ROOT, 'media', 'img', 'l10n')


# Where should this function go?
def render(s, context={}):
    t = jingo.env.from_string(s)
    return t.render(context)


@patch('django.conf.settings.LANGUAGE_CODE', 'en-US')
class TestSecureURL(TestCase):
    host = 'www.mozilla.org'
    test_path = '/firefox/partners/'
    test_view_name = 'about.partnerships.contact-bizdev'
    req = RequestFactory(HTTP_HOST=host).get(test_path)

    def _test(self, view_name, expected_url):
        eq_(render("{{ secure_url('%s') }}" % view_name, {'request': self.req}),
            expected_url)

    @patch('django.conf.settings.DEBUG', True)
    def test_on_dev_with_view_name(self):
        # Should output a reversed path
        self._test(self.test_view_name,
                   'http://' + self.host + reverse(self.test_view_name))

    @patch('django.conf.settings.DEBUG', True)
    def test_on_dev_without_view_name(self):
        # Should output the current, full URL
        self._test('', 'http://' + self.host + self.test_path)

    @patch('django.conf.settings.DEBUG', False)
    def test_on_prod_with_view_name(self):
        # Should output a reversed, full secure URL
        self._test(self.test_view_name,
                   'https://' + self.host + reverse(self.test_view_name))

    @patch('django.conf.settings.DEBUG', False)
    def test_on_prod_without_view_name(self):
        # Should output the current, full secure URL
        self._test('', 'https://' + self.host + self.test_path)

@patch('bedrock.mozorg.helpers.misc.L10N_IMG_PATH', TEST_L10N_IMG_PATH)
@patch('django.conf.settings.LANGUAGE_CODE', 'en-US')
class TestImgL10n(TestCase):
    rf = RequestFactory()

    def _render(self, locale, url):
        req = self.rf.get('/')
        req.locale = locale
        return render("{{{{ img_l10n('{0}') }}}}".format(url),
                      {'request': req})

    def test_works_for_default_lang(self):
        """Should output correct path for default lang always."""
        eq_(self._render('en-US', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/en-US/dino/head.png')

        eq_(self._render('en-US', 'dino/does-not-exist.png'),
            settings.MEDIA_URL + 'img/l10n/en-US/dino/does-not-exist.png')

    def test_works_for_other_lang(self):
        """Should use the request lang if file exists."""
        eq_(self._render('de', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/de/dino/head.png')

    def test_defaults_when_lang_file_missing(self):
        """Should use default lang when file doesn't exist for lang."""
        eq_(self._render('es', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/en-US/dino/head.png')

    @patch('bedrock.mozorg.helpers.misc.path.exists')
    def test_file_not_checked_for_default_lang(self, exists_mock):
        """
        Should not check filesystem for default lang, but should for others.
        """
        eq_(self._render('en-US', 'dino/does-not-exist.png'),
            settings.MEDIA_URL + 'img/l10n/en-US/dino/does-not-exist.png')
        ok_(not exists_mock.called)

        self._render('es', 'dino/does-not-exist.png')
        exists_mock.assert_called_once_with(os.path.join(
            TEST_L10N_IMG_PATH, 'es', 'dino', 'does-not-exist.png'))


class TestVideoTag(TestCase):
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


@patch.object(settings, 'ROOT_URLCONF', 'bedrock.mozorg.tests.urls')
class TestNewsletterFunction(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_form(self):
        response = self.client.get('/en-US/base/')
        doc = pq(response.content)
        assert_false(doc('#footer-email-errors'))
        ok_(doc('form#footer-email-form'))

    @patch('bedrock.newsletter.utils.get_newsletters')
    @patch.object(basket, 'subscribe')
    def test_post_correct_form(self, sub_mock, get_newsletters):
        get_newsletters.return_value = newsletters
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
        sub_mock.assert_called_with(
            'foo@bar.com', 'mozilla-and-you',
            format='H', country='us', lang='en',
            source_url='http://allizom.com/en-US/base/')

    @patch('bedrock.newsletter.utils.get_newsletters')
    @patch.object(basket, 'subscribe')
    def test_post_form_country_url_not_required(self, sub_mock,
                                                get_newsletters):
        """
        Form should successfully post without country or src url.
        """
        get_newsletters.return_value = newsletters
        data = {
            'newsletter-footer': 'Y',
            'newsletter': 'mozilla-and-you',
            'email': 'foo@bar.com',
            'lang': 'en',
            'fmt': 'H',
            'privacy': 'Y',
        }
        response = self.client.post('/en-US/base/', data)
        doc = pq(response.content)
        assert_false(doc('form#footer-email-form'))
        ok_(doc('div#footer-email-form.thank'))
        sub_mock.assert_called_with('foo@bar.com', 'mozilla-and-you',
                                    format='H', lang='en')

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_post_wrong_form(self, get_newsletters):
        get_newsletters.return_value = newsletters
        response = self.client.post('/en-US/base/', {'newsletter-footer': 'Y'})
        doc = pq(response.content)
        ok_(doc('#footer-email-errors'))
        ok_(doc('#footer-email-form.has-errors'))
