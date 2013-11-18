from mock import Mock

from bedrock.newsletter import utils


# patch basket client to never hit the network
# causes get_newsletters to use fallback newsletters
# in settings/newsletters.py
news_mock = Mock(side_effect=utils.basket.BasketException)
utils.basket.get_newsletters = news_mock
