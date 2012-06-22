import unittest

from nose.plugins.skip import SkipTest
from platforms import load_devices


class TestLoadDevices(unittest.TestCase):

    def file(self):
        # where should the test file go?
        return 'TODO'

    def test_load_devices(self):
        raise SkipTest
        devices = load_devices(self, self.file(), cacheDevices=False)

        #todo
