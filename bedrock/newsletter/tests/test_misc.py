import mock

from django.test.utils import override_settings

from basket import BasketException
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.utils import get_newsletters, get_languages_for_newsletters
from bedrock.newsletter.tests import newsletters


cache_mock = mock.Mock()
cache_mock.get.return_value = None
newsletters_mock = mock.Mock()
newsletters_mock.return_value = newsletters


@mock.patch('bedrock.newsletter.utils.cache', cache_mock)
class TestGetNewsletters(TestCase):
    def test_simple_get(self):
        # get_newsletters returns whatever it gets back from basket without
        # changing it at all.

        # Create a silly data structure to pass around
        test_val = {'foo': {'zoo': 'zebra'}, 'bar': {'baz': 27}}
        with mock.patch('basket.get_newsletters') as basket_get:
            basket_get.return_value = test_val
            result = get_newsletters()
        self.assertEqual(test_val, result)

    @mock.patch('basket.get_newsletters')
    def test_get_newsletters_fallback(self, mock_basket_get_newsletters):
        # if get_newsletters() cannot reach basket, it returns the
        # newsletters from settings
        mock_basket_get_newsletters.side_effect = BasketException
        default_value = mock.Mock()
        with override_settings(DEFAULT_NEWSLETTERS=default_value):
            return_value = get_newsletters()
        self.assertEqual(default_value, return_value)


@mock.patch('bedrock.newsletter.utils.cache', cache_mock)
@mock.patch('bedrock.newsletter.utils.get_newsletters', newsletters_mock)
class TestGetNewsletterLanguages(TestCase):
    def test_newsletter_langs(self):
        """Without args should return all langs."""
        result = get_languages_for_newsletters()
        good_set = set(['en', 'es', 'fr', 'de', 'pt', 'ru'])
        self.assertSetEqual(good_set, result)

    def test_single_newsletter_langs(self):
        """Should return languages for a single newsletter."""
        result = get_languages_for_newsletters('join-mozilla')
        good_set = set(['en', 'es'])
        self.assertSetEqual(good_set, result)

    def test_list_newsletter_langs(self):
        """Should return all languages for specified list of newsletters."""
        result = get_languages_for_newsletters(['join-mozilla', 'beta'])
        good_set = set(['en', 'es'])
        self.assertSetEqual(good_set, result)

        result = get_languages_for_newsletters(['firefox-tips', 'beta'])
        good_set = set(['en', 'fr', 'de', 'pt', 'ru'])
        self.assertSetEqual(good_set, result)

    def test_works_with_bad_newsletter(self):
        """If given a bad newsletter name, should still return a set."""
        result = get_languages_for_newsletters(['join-mozilla', 'eldudarino'])
        good_set = set(['en', 'es'])
        self.assertSetEqual(good_set, result)
