import unittest
import jingo
from nose.tools import eq_
from mock import Mock
from pyquery import PyQuery as pq
from product_details import product_details

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
        
        
