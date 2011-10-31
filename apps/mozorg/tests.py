import unittest
import jingo
from nose.tools import eq_
from mock import Mock
from pyquery import PyQuery as pq
from product_details import product_details

def render(s, context={}):
    t = jingo.env.from_string(s)
    return t.render(**context)

class TestDownloadButtons(unittest.TestCase):

    def test_db(self):
        latest = product_details.firefox_versions['LATEST_FIREFOX_VERSION']

        doc = pq(render('{{ download_button(LANG) }}',
                        {'request': Mock()}))

        li = doc('noscript li')
        eq_(li.length, 3);

        for a in li.find('a'):
            assert pq(a).attr('href').find('firefox-%s' % latest) != -1
        
