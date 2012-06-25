import unittest

from nose.tools import eq_, ok_, assert_not_equal
from platforms import load_devices

class TestLoadDevices(unittest.TestCase):

    def file(self):
        # where should the test file go?
        return 'TODO'

    def test_load_devices(self):
        devices = load_devices(self, self.file(), cacheDevices = False)

        #todo