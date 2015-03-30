import os.path

from mock import patch

from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings
from funfactory.helpers import static

import jingo
from funfactory.urlresolvers import reverse
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq
from rna.models import Release

from bedrock.mozorg.helpers.misc import (convert_to_high_res, releasenotes_url,
                                         absolute_url)
from bedrock.mozorg.tests import TestCase


TEST_FILES_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'test_files')
TEST_L10N_MEDIA_PATH = os.path.join(TEST_FILES_ROOT, 'media', '%s', 'l10n')

TEST_DONATE_LOCALE_LINK = {
    'default':
        'https://sendto.mozilla.org/page/contribute/Give-Now?source={source}',
    'en-US':
        'https://sendto.mozilla.org/page/contribute/givenow-seq?'
        'preset=2&source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content={source}',
    'es-MX':
        'https://sendto.mozilla.org/page/contribute/givenow-seq-es?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_ES',
}

TEST_FIREFOX_TWITTER_ACCOUNTS = {
    'en-US': 'https://twitter.com/firefox',
    'es-ES': 'https://twitter.com/firefox_es',
    'pt-BR': 'https://twitter.com/firefoxbrasil',
}


# Where should this function go?
def render(s, context=None):
    t = jingo.env.from_string(s)
    return t.render(context or {})


def test_convert_to_high_res():
    eq_(convert_to_high_res('/media/img/the.dude.png'), '/media/img/the.dude-high-res.png')
    eq_(convert_to_high_res('/media/thats-a-bummer-man.jpg'),
        '/media/thats-a-bummer-man-high-res.jpg')


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


@patch('bedrock.mozorg.helpers.misc._l10n_media_exists')
@patch('django.conf.settings.LANGUAGE_CODE', 'en-US')
class TestImgL10n(TestCase):
    rf = RequestFactory()

    def _render(self, locale, url):
        req = self.rf.get('/')
        req.locale = locale
        return render("{{{{ l10n_img('{0}') }}}}".format(url),
                      {'request': req})

    def test_works_for_default_lang(self, media_exists_mock):
        """Should output correct path for default lang always."""
        media_exists_mock.return_value = True
        eq_(self._render('en-US', 'dino/head.png'),
            static('img/l10n/en-US/dino/head.png'))

        eq_(self._render('en-US', 'dino/does-not-exist.png'),
            static('img/l10n/en-US/dino/does-not-exist.png'))

    def test_works_for_other_lang(self, media_exists_mock):
        """Should use the request lang if file exists."""
        media_exists_mock.return_value = True
        eq_(self._render('de', 'dino/head.png'),
            static('img/l10n/de/dino/head.png'))

    def test_defaults_when_lang_file_missing(self, media_exists_mock):
        """Should use default lang when file doesn't exist for lang."""
        media_exists_mock.return_value = False
        eq_(self._render('is', 'dino/head.png'),
            static('img/l10n/en-US/dino/head.png'))

    def test_latam_spanishes_fallback_to_european_spanish(self, media_exists_mock):
        """Should use es-ES image when file doesn't exist for lang."""
        media_exists_mock.side_effect = [False, True]
        eq_(self._render('es-AR', 'dino/head.png'),
            static('img/l10n/es-ES/dino/head.png'))

        media_exists_mock.reset_mock()
        media_exists_mock.side_effect = [False, True]
        eq_(self._render('es-CL', 'dino/head.png'),
            static('img/l10n/es-ES/dino/head.png'))

        media_exists_mock.reset_mock()
        media_exists_mock.side_effect = [False, True]
        eq_(self._render('es-MX', 'dino/head.png'),
            static('img/l10n/es-ES/dino/head.png'))

        media_exists_mock.reset_mock()
        media_exists_mock.side_effect = [False, True]
        eq_(self._render('es', 'dino/head.png'),
            static('img/l10n/es-ES/dino/head.png'))

    def test_file_not_checked_for_default_lang(self, media_exists_mock):
        """
        Should not check filesystem for default lang, but should for others.
        """
        eq_(self._render('en-US', 'dino/does-not-exist.png'),
            static('img/l10n/en-US/dino/does-not-exist.png'))
        ok_(not media_exists_mock.called)

        self._render('is', 'dino/does-not-exist.png')
        media_exists_mock.assert_called_once_with('img', 'is', 'dino/does-not-exist.png')


@override_settings(DEBUG=False)
@patch('bedrock.mozorg.helpers.misc._l10n_media_exists')
class TestL10nCSS(TestCase):
    rf = RequestFactory()
    static_url_dev = '/static/'
    cdn_url = '//mozorg.cdn.mozilla.net'
    static_url_prod = cdn_url + static_url_dev
    markup = ('<link rel="stylesheet" media="screen,projection,tv" href='
              '"%scss/l10n/%s/intl.css">')

    def _render(self, locale):
        req = self.rf.get('/')
        req.locale = locale
        return render('{{ l10n_css() }}', {'request': req})

    @override_settings(DEV=True)
    @patch('django.contrib.staticfiles.storage.staticfiles_storage.base_url', static_url_dev)
    def test_dev_when_css_file_exists(self, media_exists_mock):
        """Should output a path to the CSS file if exists."""
        media_exists_mock.return_value = True
        eq_(self._render('de'), self.markup % (self.static_url_dev, 'de'))
        eq_(self._render('es-ES'), self.markup % (self.static_url_dev, 'es-ES'))

    @override_settings(DEV=True)
    def test_dev_when_css_file_missing(self, media_exists_mock):
        """Should output nothing if the CSS file is missing."""
        media_exists_mock.return_value = False
        eq_(self._render('en-US'), '')
        eq_(self._render('fr'), '')

    @override_settings(DEV=False)
    @patch('django.contrib.staticfiles.storage.staticfiles_storage.base_url', static_url_prod)
    def test_prod_when_css_file_exists(self, media_exists_mock):
        """Should output a path to the CSS file if exists."""
        media_exists_mock.return_value = True
        eq_(self._render('de'), self.markup % (self.static_url_prod, 'de'))
        eq_(self._render('es-ES'), self.markup % (self.static_url_prod, 'es-ES'))

    @override_settings(DEV=False)
    def test_prod_when_css_file_missing(self, media_exists_mock):
        """Should output nothing if the CSS file is missing."""
        media_exists_mock.return_value = False
        eq_(self._render('en-US'), '')
        eq_(self._render('fr'), '')


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


@override_settings(STATIC_URL='/media/')
@patch('bedrock.mozorg.helpers.misc.find_static', return_value=True)
class TestPlatformImg(TestCase):
    rf = RequestFactory()

    def _render(self, url, optional_attributes=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ platform_img('{0}', {1}) }}}}".format(url, optional_attributes),
                      {'request': req})

    def _render_l10n(self, url):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ l10n_img('{0}') }}}}".format(url),
                      {'request': req})

    def test_platform_img_no_optional_attributes(self, find_static):
        """Should return expected markup without optional attributes"""
        markup = self._render('test.png')
        self.assertIn(u'data-src-windows="/media/test-windows.png"', markup)
        self.assertIn(u'data-src-mac="/media/test-mac.png"', markup)

    def test_platform_img_with_optional_attributes(self, find_static):
        """Should return expected markup with optional attributes"""
        markup = self._render('test.png', {'data-test-attr': 'test'})
        self.assertIn(u'data-test-attr="test"', markup)

    def test_platform_img_with_high_res(self, find_static):
        """Should return expected markup with high resolution image attrs"""
        markup = self._render('test.png', {'high-res': True})
        self.assertIn(u'data-src-windows-high-res="/media/test-windows-high-res.png"', markup)
        self.assertIn(u'data-src-mac-high-res="/media/test-mac-high-res.png"', markup)
        self.assertIn(u'data-high-res="true"', markup)

    def test_platform_img_with_l10n(self, find_static):
        """Should return expected markup with l10n image path"""
        l10n_url_win = self._render_l10n('test-windows.png')
        l10n_url_mac = self._render_l10n('test-mac.png')
        markup = self._render('test.png', {'l10n': True})
        self.assertIn(u'data-src-windows="' + l10n_url_win + '"', markup)
        self.assertIn(u'data-src-mac="' + l10n_url_mac + '"', markup)

    def test_platform_img_with_l10n_and_optional_attributes(self, find_static):
        """
        Should return expected markup with l10n image path and optional
        attributes
        """
        l10n_url_win = self._render_l10n('test-windows.png')
        l10n_url_mac = self._render_l10n('test-mac.png')
        markup = self._render('test.png', {'l10n': True, 'data-test-attr': 'test'})
        self.assertIn(u'data-src-windows="' + l10n_url_win + '"', markup)
        self.assertIn(u'data-src-mac="' + l10n_url_mac + '"', markup)
        self.assertIn(u'data-test-attr="test"', markup)

    def test_platform_img_with_l10n_and_high_res(self, find_static):
        """
        Should return expected markup with l10n image path and high resolution
        attributes
        """
        l10n_url_win = self._render_l10n('test-windows.png')
        l10n_hr_url_win = convert_to_high_res(l10n_url_win)
        l10n_url_mac = self._render_l10n('test-mac.png')
        l10n_hr_url_mac = convert_to_high_res(l10n_url_mac)
        markup = self._render('test.png', {'l10n': True, 'high-res': True})
        self.assertIn(u'data-src-windows-high-res="' + l10n_hr_url_win + '"', markup)
        self.assertIn(u'data-src-mac-high-res="' + l10n_hr_url_mac + '"', markup)
        self.assertIn(u'data-high-res="true"', markup)


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


@override_settings(DONATE_LOCALE_LINK=TEST_DONATE_LOCALE_LINK)
class TestDonateUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale, source=''):
        req = self.rf.get('/')
        req.locale = locale
        return render("{{{{ donate_url('{0}') }}}}".format(source),
                      {'request': req})

    def test_donate_url_no_locale(self):
        """No locale, fallback to default page"""
        eq_(self._render('', 'mozillaorg_footer'),
            'https://sendto.mozilla.org/page/contribute/Give-Now?'
            'source=mozillaorg_default_footer')

    def test_donate_url_english(self):
        """en-US locale, default page"""
        eq_(self._render('en-US', 'mozillaorg_footer'),
            'https://sendto.mozilla.org/page/contribute/givenow-seq?'
            'preset=2&amp;source=mozillaorg_footer&amp;ref=EOYFR2014'
            '&amp;utm_campaign=EOYFR2014&amp;utm_source=mozilla.org'
            '&amp;utm_medium=referral&amp;utm_content=mozillaorg_footer')

    def test_donate_url_spanish(self):
        """es-MX locale, a localized page"""
        eq_(self._render('es-MX', 'mozillaorg_footer'),
            'https://sendto.mozilla.org/page/contribute/givenow-seq-es?'
            'source=mozillaorg_footer&amp;ref=EOYFR2014'
            '&amp;utm_campaign=EOYFR2014&amp;utm_source=mozilla.org&amp;'
            'utm_medium=referral&amp;utm_content=mozillaorg_ES')

    def test_donate_url_other_locale(self):
        """No page for locale, fallback to default page"""
        eq_(self._render('pt-PT', 'mozillaorg_footer'),
            'https://sendto.mozilla.org/page/contribute/Give-Now?'
            'source=mozillaorg_default_footer')


@override_settings(FIREFOX_TWITTER_ACCOUNTS=TEST_FIREFOX_TWITTER_ACCOUNTS)
class TestFirefoxTwitterUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get('/')
        req.locale = locale
        return render('{{ firefox_twitter_url() }}', {'request': req})

    def test_firefox_twitter_url_no_locale(self):
        """No locale, fallback to default account"""
        eq_(self._render(''), 'https://twitter.com/firefox')

    def test_firefox_twitter_url_english(self):
        """en-US locale, default account"""
        eq_(self._render('en-US'), 'https://twitter.com/firefox')

    def test_firefox_twitter_url_spanish(self):
        """es-ES locale, a local account"""
        eq_(self._render('es-ES'), 'https://twitter.com/firefox_es')

    def test_firefox_twitter_url_portuguese(self):
        """pt-BR locale, a local account"""
        eq_(self._render('pt-BR'), 'https://twitter.com/firefoxbrasil')

    def test_firefox_twitter_url_other_locale(self):
        """No account for locale, fallback to default account"""
        eq_(self._render('es-AR'), 'https://twitter.com/firefox')
        eq_(self._render('es-CL'), 'https://twitter.com/firefox')
        eq_(self._render('es-MX'), 'https://twitter.com/firefox')
        eq_(self._render('pt-PT'), 'https://twitter.com/firefox')


@override_settings(STATIC_URL='/media/')
class TestHighResImg(TestCase):
    rf = RequestFactory()

    def _render(self, url, optional_attributes=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ high_res_img('{0}', {1}) }}}}".format(url, optional_attributes),
                      {'request': req})

    def _render_l10n(self, url):
        req = self.rf.get('/')
        req.locale = 'en-US'
        return render("{{{{ l10n_img('{0}') }}}}".format(url),
                      {'request': req})

    def test_high_res_img_no_optional_attributes(self):
        """Should return expected markup without optional attributes"""
        markup = self._render('test.png')
        expected = (
            u'<img class="js" src="" data-processed="false" data-src="/media/test.png" '
            u'data-high-res="true" data-high-res-src="/media/test-high-res.png">'
            u'<noscript><img src="/media/test.png"></noscript>')
        self.assertEqual(markup, expected)

    def test_high_res_img_with_optional_attributes(self):
        """Should return expected markup with optional attributes"""
        markup = self._render('test.png', {'data-test-attr': 'test'})
        expected = (
            u'<img class="js" src="" data-processed="false" data-src="/media/test.png" '
            u'data-high-res="true" data-high-res-src="/media/test-high-res.png" '
            u'data-test-attr="test"><noscript>'
            u'<img src="/media/test.png" data-test-attr="test"></noscript>')
        self.assertEqual(markup, expected)

    def test_high_res_img_with_l10n(self):
        """Should return expected markup with l10n image path"""
        l10n_url = self._render_l10n('test.png')
        l10n_hr_url = convert_to_high_res(l10n_url)
        markup = self._render('test.png', {'l10n': True})
        expected = (
            u'<img class="js" src="" data-processed="false" data-src="' + l10n_url + '" '
            u'data-high-res="true" data-high-res-src="' + l10n_hr_url + '">'
            u'<noscript><img src="' + l10n_url + '"></noscript>')
        self.assertEqual(markup, expected)

    def test_high_res_img_with_l10n_and_optional_attributes(self):
        """Should return expected markup with l10n image path"""
        l10n_url = self._render_l10n('test.png')
        l10n_hr_url = convert_to_high_res(l10n_url)
        markup = self._render('test.png', {'l10n': True, 'data-test-attr': 'test'})
        expected = (
            u'<img class="js" src="" data-processed="false" data-src="' + l10n_url + '" '
            u'data-high-res="true" data-high-res-src="' + l10n_hr_url + '" data-test-attr="test">'
            u'<noscript><img src="' + l10n_url + '" data-test-attr="test">'
            u'</noscript>')
        self.assertEqual(markup, expected)


class TestAbsoluteURLFilter(TestCase):
    rf = RequestFactory()
    static_url_dev = '/static/'
    static_url_prod = '//mozorg.cdn.mozilla.net/static/'
    static_url_full = 'https://mozorg.cdn.mozilla.net/static/'
    image_path = 'img/mozorg/mozilla-256.jpg'
    inline_template = "{{ static('%s')|absolute_url }}" % image_path
    block_template = ("{% filter absolute_url %}{% block page_image %}" +
                      "{{ static('%s') }}" % image_path + "{% endblock %}{% endfilter %}")

    def _render(self, template):
        return render(template, {'request': self.rf.get('/')})

    @patch('django.contrib.staticfiles.storage.staticfiles_storage.base_url', static_url_dev)
    def test_image_dev(self):
        """Should return a fully qualified URL including a protocol"""
        expected = settings.CANONICAL_URL + self.static_url_dev + self.image_path
        eq_(self._render(self.inline_template), expected)
        eq_(self._render(self.block_template), expected)

    @patch('django.contrib.staticfiles.storage.staticfiles_storage.base_url', static_url_prod)
    def test_image_prod(self):
        """Should return a fully qualified URL including a protocol"""
        expected = 'https:' + self.static_url_prod + self.image_path
        eq_(self._render(self.inline_template), expected)
        eq_(self._render(self.block_template), expected)

    @override_settings(DEV=False)
    def test_urls(self):
        """Should return a fully qualified URL including a protocol"""
        expected = 'https://www.mozilla.org/en-US/firefox/new/'
        eq_(absolute_url('/en-US/firefox/new/'), expected)
        eq_(absolute_url('//www.mozilla.org/en-US/firefox/new/'), expected)
        eq_(absolute_url('https://www.mozilla.org/en-US/firefox/new/'), expected)


class TestReleaseNotesURL(TestCase):
    @patch('bedrock.mozorg.helpers.misc.reverse')
    def test_aurora_android_releasenotes_url(self, mock_reverse):
        """
        Should return the results of reverse with the correct args
        """
        release = Release(
            channel='Aurora', version='42.0a2', product='Firefox for Android')
        eq_(releasenotes_url(release), mock_reverse.return_value)
        mock_reverse.assert_called_with(
            'mobile.releasenotes', args=('42.0a2', 'aurora'))

    @patch('bedrock.mozorg.helpers.misc.reverse')
    def test_desktop_releasenotes_url(self, mock_reverse):
        """
        Should return the results of reverse with the correct args
        """
        release = Release(version='42.0', product='Firefox')
        eq_(releasenotes_url(release), mock_reverse.return_value)
        mock_reverse.assert_called_with(
            'firefox.releasenotes', args=('42.0', 'release'))

    @patch('bedrock.mozorg.helpers.misc.reverse')
    def test_firefox_os_releasenotes_url(self, mock_reverse):
        """
        Should return the results of reverse with the correct args
        """
        release = Release(version='42.0', product='Firefox OS')
        eq_(releasenotes_url(release), mock_reverse.return_value)
        mock_reverse.assert_called_with(
            'firefox.os.releasenotes', args=['42.0'])
