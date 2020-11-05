from bedrock.sitemaps.models import NO_LOCALE, SitemapURL
from bedrock.mozorg.tests import TestCase


class TestSitemapsModel(TestCase):
    def test_absolute_url(self):
        obj = SitemapURL(path='/firefox/',
                         locale='de')
        assert obj.get_absolute_url() == 'https://www.mozilla.org/de/firefox/'
        # none locale
        obj = SitemapURL(path='/firefox/',
                         locale=NO_LOCALE)
        assert obj.get_absolute_url() == 'https://www.mozilla.org/firefox/'

    def test_all_for_locale(self):
        SitemapURL.objects.create(path='/firefox/',
                                  locale='de')
        SitemapURL.objects.create(path='/firefox/',
                                  locale='fr')
        SitemapURL.objects.create(path='/',
                                  locale='de')
        SitemapURL.objects.create(path='/about/',
                                  locale='de')
        de_paths = [str(o) for o in SitemapURL.objects.all_for_locale('de')]
        # should contain no fr URL and be in alphabetical order
        assert de_paths == ['/de/', '/de/about/', '/de/firefox/']

    def test_all_locales(self):
        SitemapURL.objects.create(path='/firefox/',
                                  locale='de')
        SitemapURL.objects.create(path='/firefox/',
                                  locale='fr')
        SitemapURL.objects.create(path='/',
                                  locale='de')
        SitemapURL.objects.create(path='/firefox/',
                                  locale='en-US')
        SitemapURL.objects.create(path='/locales/',
                                  locale=NO_LOCALE)
        assert list(SitemapURL.objects.all_locales()) == [NO_LOCALE, 'de', 'en-US', 'fr']
