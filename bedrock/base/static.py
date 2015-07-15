from whitenoise.django import DjangoWhiteNoise


class BedrockWhiteNoise(DjangoWhiteNoise):
    """WhiteNoise class for modifying default cache headers."""
    ONE_MONTH = 30 * 24 * 60 * 60

    def add_cache_headers(self, static_file, url):
        if self.is_immutable_file(static_file, url):
            max_age = self.FOREVER
        elif '/fonts/' in url:
            max_age = self.ONE_MONTH
        else:
            max_age = self.max_age
        if max_age is not None:
            cache_control = 'public, max-age={}'.format(max_age)
            static_file.headers['Cache-Control'] = cache_control
