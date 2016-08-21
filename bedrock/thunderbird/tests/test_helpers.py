from django.test.client import RequestFactory

from django_jinja.backend import Jinja2
from nose.tools import eq_
from pyquery import PyQuery as pq

from bedrock.mozorg.tests import TestCase


jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


class TestDownloadButtons(TestCase):

    def test_thunderbird(self):
        """Should have 4 links on the Thunderbird download button"""
        with self.activate('en-US'):
            rf = RequestFactory()
            get_request = rf.get('/fake')
            get_request.locale = 'en-US'
            doc = pq(render("{{ download_thunderbird() }}",
                            {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 4)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux')
        eq_(pq(list[3]).attr('class'), 'os_linux64')

    def test_beta(self):
        """Should have 4 links on the Thunderbird Beta download button"""
        with self.activate('en-US'):
            rf = RequestFactory()
            get_request = rf.get('/fake')
            get_request.locale = 'en-US'
            doc = pq(render("{{ download_thunderbird('beta') }}",
                            {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 4)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux')
        eq_(pq(list[3]).attr('class'), 'os_linux64')

    def test_earlybird(self):
        """Should have 4 links on the Earlybird download button"""
        with self.activate('en-US'):
            rf = RequestFactory()
            get_request = rf.get('/fake')
            get_request.locale = 'en-US'
            doc = pq(render("{{ download_thunderbird('alpha') }}",
                            {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 4)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux')
        eq_(pq(list[3]).attr('class'), 'os_linux64')


class TestThunderbirdURL(TestCase):
    rf = RequestFactory()

    def _render(self, page, channel=None):
        with self.activate('en-US'):
            req = self.rf.get('/')
            req.locale = 'en-US'
            if channel:
                tmpl = "{{ thunderbird_url('%s', '%s') }}" % (page, channel)
            else:
                tmpl = "{{ thunderbird_url('%s') }}" % page
            return render(tmpl, {'request': req})

    def test_thunderbird_all(self):
        """Should return a reversed path for the Thunderbird download page"""
        eq_(self._render('all'),
            '/en-US/thunderbird/all/')
        eq_(self._render('all', 'release'),
            '/en-US/thunderbird/all/')
        eq_(self._render('all', 'beta'),
            '/en-US/thunderbird/beta/all/')
        eq_(self._render('all', 'alpha'),
            '/en-US/thunderbird/earlybird/all/')

    def test_thunderbird_sysreq(self):
        """Should return a reversed path for the Thunderbird sysreq page"""
        eq_(self._render('sysreq'),
            '/en-US/thunderbird/system-requirements/')
        eq_(self._render('sysreq', 'release'),
            '/en-US/thunderbird/system-requirements/')
        eq_(self._render('sysreq', 'beta'),
            '/en-US/thunderbird/beta/system-requirements/')
        eq_(self._render('sysreq', 'alpha'),
            '/en-US/thunderbird/earlybird/system-requirements/')

    def test_thunderbird_notes(self):
        """Should return a reversed path for the desktop notes page"""
        eq_(self._render('notes'),
            '/en-US/thunderbird/notes/')
        eq_(self._render('notes', 'release'),
            '/en-US/thunderbird/notes/')
        eq_(self._render('notes', 'beta'),
            '/en-US/thunderbird/beta/notes/')
        eq_(self._render('notes', 'alpha'),
            '/en-US/thunderbird/earlybird/notes/')
