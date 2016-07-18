import mock

from basket import BasketException, errors
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter import utils
from bedrock.newsletter.tests import newsletters


cache_mock = mock.Mock()
cache_mock.get.return_value = None
newsletters_mock = mock.Mock()
newsletters_mock.return_value = newsletters


@mock.patch('bedrock.newsletter.utils.cache', cache_mock)
class TestGetNewsletters(TestCase):
    def setUp(self):
        utils.NEWSLETTERS_LOCAL_DATA = None

    def test_simple_get(self):
        # get_newsletters returns whatever it gets back from basket without
        # changing it at all.

        # Create a silly data structure to pass around
        test_val = {'foo': {'zoo': 'zebra'}, 'bar': {'baz': 27}}
        with mock.patch('basket.get_newsletters') as basket_get:
            basket_get.return_value = test_val
            result = utils.get_newsletters()
        self.assertEqual(test_val, result)

    @mock.patch('bedrock.newsletter.utils.get_local_basket_newsletters_data')
    @mock.patch('basket.get_newsletters')
    def test_get_newsletters_fallback(self, mock_basket_get_newsletters, mock_glbnd):
        # if get_newsletters() cannot reach basket, it returns the
        # newsletters from cached json
        mock_basket_get_newsletters.side_effect = BasketException(
            'network error',
            code=errors.BASKET_NETWORK_FAILURE,
        )
        return_value = utils.get_newsletters()
        self.assertEqual(mock_glbnd.return_value, return_value)

    @mock.patch.object(utils, 'json')
    def test_get_local_basket_newsletters_data(self, mock_json):
        """Should only call json.loads once"""
        utils.get_local_basket_newsletters_data()
        utils.get_local_basket_newsletters_data()
        mock_json.load.assert_called_once()

    def test_get_local_basket_newsletters_data_works(self):
        """Should load json without error"""
        data = utils.get_local_basket_newsletters_data()
        self.assertIn('mozilla-and-you', data)
        self.assertIn('mozilla-foundation', data)


@mock.patch('bedrock.newsletter.utils.cache', cache_mock)
@mock.patch('bedrock.newsletter.utils.get_newsletters', newsletters_mock)
class TestGetNewsletterLanguages(TestCase):
    def test_newsletter_langs(self):
        """Without args should return all langs."""
        result = utils.get_languages_for_newsletters()
        good_set = {'en', 'es', 'fr', 'de', 'pt', 'ru'}
        self.assertSetEqual(good_set, result)

    def test_single_newsletter_langs(self):
        """Should return languages for a single newsletter."""
        result = utils.get_languages_for_newsletters('join-mozilla')
        good_set = {'en', 'es'}
        self.assertSetEqual(good_set, result)

    def test_list_newsletter_langs(self):
        """Should return all languages for specified list of newsletters."""
        result = utils.get_languages_for_newsletters(['join-mozilla', 'beta'])
        good_set = {'en', 'es'}
        self.assertSetEqual(good_set, result)

        result = utils.get_languages_for_newsletters(['firefox-tips', 'beta'])
        good_set = {'en', 'fr', 'de', 'pt', 'ru'}
        self.assertSetEqual(good_set, result)

    def test_works_with_bad_newsletter(self):
        """If given a bad newsletter name, should still return a set."""
        result = utils.get_languages_for_newsletters(['join-mozilla', 'eldudarino'])
        good_set = {'en', 'es'}
        self.assertSetEqual(good_set, result)
