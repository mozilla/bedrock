import os.path

from mock import patch

from django.conf import settings
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings

import basket
import jingo
import jinja2
from nose.tools import assert_false, eq_, ok_
from pyquery import PyQuery as pq
from bedrock.newsletter.tests.test_views import newsletters
from funfactory.urlresolvers import reverse

from bedrock.mozorg.helpers.misc import platform_img
from bedrock.mozorg.helpers.misc import high_res_img
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
    test_view_name = 'mozorg.partnerships'
    req = RequestFactory(HTTP_HOST=host).get(test_path)
    secure_req = RequestFactory(HTTP_HOST=host).get(test_path, {}, **{'wsgi.url_scheme': 'https'})

    def _test(self, view_name, expected_url, ssl):
        eq_(render("{{ secure_url('%s') }}" % view_name, {'request': (self.secure_req if ssl else self.req)}),
            expected_url)

    def test_no_ssl_with_view_name(self):
        # Should output a reversed path without https
        self._test(self.test_view_name,
                   'http://' + self.host + reverse(self.test_view_name), False)

    def test_no_ssl_without_view_name(self):
        # Should output the current, full URL without https
        self._test('', 'http://' + self.host + self.test_path, False)

    def test_ssl_with_view_name(self):
        # Should output a reversed, full secure URL
        self._test(self.test_view_name,
                   'https://' + self.host + reverse(self.test_view_name), True)

    def test_ssl_without_view_name(self):
        # Should output the current, full secure URL
        self._test('', 'https://' + self.host + self.test_path, True)


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
        eq_(self._render('is', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/en-US/dino/head.png')

    def test_latam_spanishes_fallback_to_european_spanish(self):
        """Should use es-ES image when file doesn't exist for lang."""
        eq_(self._render('es-AR', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/es-ES/dino/head.png')
        eq_(self._render('es-CL', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/es-ES/dino/head.png')
        eq_(self._render('es-MX', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/es-ES/dino/head.png')
        eq_(self._render('es', 'dino/head.png'),
            settings.MEDIA_URL + 'img/l10n/es-ES/dino/head.png')

    @patch('bedrock.mozorg.helpers.misc.path.exists')
    def test_file_not_checked_for_default_lang(self, exists_mock):
        """
        Should not check filesystem for default lang, but should for others.
        """
        eq_(self._render('en-US', 'dino/does-not-exist.png'),
            settings.MEDIA_URL + 'img/l10n/en-US/dino/does-not-exist.png')
        ok_(not exists_mock.called)

        self._render('is', 'dino/does-not-exist.png')
        exists_mock.assert_called_once_with(os.path.join(
            TEST_L10N_IMG_PATH, 'is', 'dino', 'does-not-exist.png'))


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


class TestPlatformImg(TestCase):
    @override_settings(MEDIA_URL='/media/')
    def test_platform_img_no_optional_attributes(self):
        """Should return expected markup without optional attributes"""
        markup = platform_img('test.png')
        expected = (
            u'<img class="platform-img js" src="" data-src="/media/test.png" >'
            u'<noscript><img class="platform-img win" src="/media/test.png" >'
            u'</noscript>')
        self.assertEqual(markup, jinja2.Markup(expected))

    @override_settings(MEDIA_URL='/media/')
    def test_platform_img_with_optional_attributes(self):
        """Should return expected markup with optional attributes"""
        markup = platform_img('test.png', {'data-test-attr': 'test'})
        expected = (
            u'<img class="platform-img js" src="" data-src="/media/test.png" '
            u'data-test-attr="test"><noscript><img class="platform-img win" '
            u'src="/media/test.png" data-test-attr="test"></noscript>')
        self.assertEqual(markup, jinja2.Markup(expected))


class TestPressBlogUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get('/')
        req.locale = locale
        return render("{{{{ press_blog_url() }}}}".format('/'),
                      {'request': req})

    def test_press_blog_url_no_locale(self):
        """No locale, fallback to default press blog"""
        eq_(self._render(''), 'https://blog.mozilla.org/press/')

    def test_press_blog_url_english(self):
        """en-US locale, default press blog"""
        eq_(self._render('en-US'), 'https://blog.mozilla.org/press/')

    def test_press_blog_url_europe(self):
        """Major European locales have their own blog"""
        eq_(self._render('es-ES'), 'https://blog.mozilla.org/press-es/')
        eq_(self._render('fr'), 'https://blog.mozilla.org/press-fr/')
        eq_(self._render('de'), 'https://blog.mozilla.org/press-de/')
        eq_(self._render('pl'), 'https://blog.mozilla.org/press-pl/')
        eq_(self._render('it'), 'https://blog.mozilla.org/press-it/')
        eq_(self._render('en-GB'), 'https://blog.mozilla.org/press-uk/')

    def test_press_blog_url_latam(self):
        """South American Spanishes have a specific blog"""
        eq_(self._render('es-AR'), 'https://blog.mozilla.org/press-latam/')
        eq_(self._render('es-CL'), 'https://blog.mozilla.org/press-latam/')
        eq_(self._render('es-MX'), 'https://blog.mozilla.org/press-latam/')

    def test_press_blog_url_other_locale(self):
        """No blog for locale, fallback to default press blog"""
        eq_(self._render('oc'), 'https://blog.mozilla.org/press/')


class TestHighResImg(TestCase):
    @override_settings(MEDIA_URL='/media/')
    def test_high_res_img_no_optional_attributes(self):
        """Should return expected markup without optional attributes"""
        markup = high_res_img('test.png')
        expected = (
            u'<img class="js" src="" data-src="/media/test.png" '
            u'data-high-res="true" >'
            u'<noscript><img src="/media/test.png" ></noscript>')
        self.assertEqual(markup, jinja2.Markup(expected))

    @override_settings(MEDIA_URL='/media/')
    def test_high_res_img_with_optional_attributes(self):
        """Should return expected markup with optional attributes"""
        markup = high_res_img('test.png', {'data-test-attr': 'test'})
        expected = (
            u'<img class="js" src="" data-src="/media/test.png" '
            u'data-high-res="true" data-test-attr="test">'
            u'<noscript><img src="/media/test.png" data-test-attr="test">'
            u'</noscript>')
        self.assertEqual(markup, jinja2.Markup(expected))


class TestAbsoluteURLFilter(TestCase):
    rf = RequestFactory()
    media_url_dev = '/media/'
    media_url_prod = '//mozorg.cdn.mozilla.net/media/'
    image_path = 'img/mozorg/mozilla-256.jpg'
    inline_template = "{{ media('%s')|absolute_url }}" % image_path
    block_template = ("{% filter absolute_url %}{% block page_image %}" +
        "{{ media('%s') }}" % image_path + "{% endblock %}{% endfilter %}")

    def _render(self, template):
        return render(template, {'request': self.rf.get('/')})

    @override_settings(MEDIA_URL=media_url_dev)
    def test_dev(self):
        """Should return a fully qualified URL including a protocol"""
        expected = settings.CANONICAL_URL + self.media_url_dev + self.image_path
        eq_(self._render(self.inline_template), expected)
        eq_(self._render(self.block_template), expected)

    @override_settings(MEDIA_URL=media_url_prod)
    def test_prod(self):
        """Should return a fully qualified URL including a protocol"""
        expected = 'https:' + self.media_url_prod + self.image_path
        eq_(self._render(self.inline_template), expected)
        eq_(self._render(self.block_template), expected)
