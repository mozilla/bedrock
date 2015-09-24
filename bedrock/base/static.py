import os.path

from whitenoise.django import DjangoWhiteNoise


class BedrockWhiteNoise(DjangoWhiteNoise):
    """WhiteNoise class for modifying default cache headers."""
    ONE_MONTH = 30 * 24 * 60 * 60

    def __init__(self, application):
        super(BedrockWhiteNoise, self).__init__(application)

        # TODO add tests for these in mcom-tests
        # So that current calendar subscriptions will continue to work
        static_root = self.get_static_root_and_prefix()[0]
        self.add_files(os.path.join(static_root, 'caldata'),
                       prefix='projects/calendar/caldata/')

    def add_cache_headers(self, static_file, url):
        if self.is_immutable_file(static_file, url):
            max_age = self.FOREVER
        # files typically accessed not by hashed name
        elif '/fonts/' in url or '/caldata/' in url:
            max_age = self.ONE_MONTH
        else:
            max_age = self.max_age
        if max_age is not None:
            cache_control = 'public, max-age={}'.format(max_age)
            static_file.headers['Cache-Control'] = cache_control
