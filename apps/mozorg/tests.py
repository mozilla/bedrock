import unittest

import jingo
from mock import Mock
from nose.tools import eq_, ok_
from product_details import product_details
from pyquery import PyQuery as pq


# Where should this function go?
def render(s, context={}):
    t = jingo.env.from_string(s)
    return t.render(**context)


class TestDownloadButtons(unittest.TestCase):

    def latest_version(self):
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def check_platform_links(self, links):
        key = 'firefox-%s' % self.latest_version()

        # Make sure the first three links have the correct firefox
        # version in them
        for link in links:
            assert pq(link).attr('href').find(key) != -1

    def check_dumb_button(self, doc):
        # Make sure 4 links are present (3 platform links and 1 link
        # to a special page for unsupported platforms)
        links = doc('li a')
        eq_(links.length, 4);

        self.check_platform_links(links[:3])

        # Check the link for unsupported platforms
        h = pq(links[3]).attr('href')
        assert h.find(self.latest_version()) != -1
        assert h.find('releasenotes') != -1

    def test_button(self, format='large'):
        doc = pq(render("{{ download_button('button', '%s') }}" % format,
                        {'request': Mock()}))

        eq_(doc.attr('id'), 'button')

        self.check_dumb_button(doc('noscript'))
        self.check_dumb_button(doc('ul.unsupported-download'))

        # 3 platform links should be present
        links = doc('.home-download li a')
        eq_(links.length, 3)

        self.check_platform_links(links)

    def test_small_button(self):
        self.test_button('small')


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
        videos = [self.nomoz_video % ext for ext in ('ogv', 'exe', 'webm', 'txt')]
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
