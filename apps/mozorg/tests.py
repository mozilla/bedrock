# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from test_utils import RequestFactory

import jingo
from nose.tools import eq_, ok_, assert_not_equal
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
