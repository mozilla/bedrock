import mock

from django.test.utils import override_settings

from basket import BasketException
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.utils import (
    clear_caches, get_newsletters, get_newsletter_languages)


class TestGetnewsletters(TestCase):
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
        clear_caches()
        with override_settings(DEFAULT_NEWSLETTERS=default_value):
            return_value = get_newsletters()
        self.assertEqual(default_value, return_value)

    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_newsletter_langs(self, mock_get_newsletters):
        # test get_newsletter_languages
        clear_caches()
        mock_get_newsletters.return_value = {
            'aaa': {'languages': ['aa', 'bb']},
            'bbb': {'languages': ['aa-YY', 'cc-XX']},
            'ccc': {}
        }
        result = get_newsletter_languages()
        self.assertEqual(set(['aa', 'bb', 'cc']), result)
