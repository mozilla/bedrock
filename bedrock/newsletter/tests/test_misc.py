import mock

from bedrock.mozorg.tests import TestCase

from bedrock.newsletter.utils import get_newsletters


class TestGetnewsletters(TestCase):
    def test_simple_get(self):
        # get_newsletters returns whatever it gets back from basket without
        # changing it at all.

        # Create a silly data structure to pass around
        test_val = {'foo': [1, 2, 3], 'bar': {'baz': 27}}
        with mock.patch('basket.get_newsletters') as basket_get:
            basket_get.return_value = test_val
            result = get_newsletters()
        self.assertEqual(test_val, result)
