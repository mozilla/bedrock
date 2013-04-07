# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv
from operator import itemgetter

from django.core.cache import cache
from django.core.files import File

def case_insensitive_in(self, collection, value):
    """Check a collection for a string value ignoring case."""
    for i in collection:
        if value.lower() == i.lower():
            return True

    return False


def load_devices(self, file, cacheDevices=True):
    """Load devices from a source csv, returning device names in a
    nested dict by platform and manufacturer with manufacturer and
    devices sorted.

    Accepted kwargs:
    file -- location of the csv to load
    cacheDevices -- whether or not to cache the loaded devices (default True)

    Source csv is expected to be comma delimited, properly escaped, and contain
    a header row, and the following required columns:
    platform, manufacturer, device.

    Platforms outside of 'Phone' and 'Tablet' are ignored. Duplicates
    are ignored. Comparison is case-insensitive with leading and
    trailing white space removed. The first instance of a device in the
    csv will be used for displayed capitalization of a manufacturer or
    device.
    """
    devices = None
    if cacheDevices is True:
        devices = cache.get('devices')

    if devices is None:
        # List of supported platforms. Any row in the csv that doesn't
        # match one of these platforms will be ignored. Change this if
        # the csv should define the platforms.
        platforms = ['Phone', 'Tablet']
        devices = dict()
        for platform in platforms:
            devices[platform] = dict()

        with open(file, 'rb') as file:
            reader = csv.DictReader(file, delimiter = ',',
                                    skipinitialspace = True)

            # Strip leading and trailing whitespace from each value to
            # normalize values in the csv. This prevents whitespace
            # from creating double entries for any
            # platform/manufacturer/device combination.
            reader = (dict((k, v.strip()) for k, v in row.items())
                      for row in reader)

            try:
                for row in reader:
                    # Local variables for code readability.
                    platform = row['platform']
                    manufacturer = row['manufacturer']
                    device = row['device']

                    if not case_insensitive_in(self, devices, platform):
                        continue

                    # Store the manufacturers in a list so they can
                    # easily be access after being sorted. Init the
                    # list when it's a new platform.
                    if 'manufacturers' not in devices[platform]:
                        devices[platform]['manufacturers'] = []

                    # Add new manufacturers to the list.
                    if not case_insensitive_in(self,
                                               devices[platform]['manufacturers'],
                                               manufacturer):
                        devices[platform]['manufacturers'].append(manufacturer)

                    # Init the list of devices for a new manufacturer.
                    if not case_insensitive_in(self,
                                               devices[platform], manufacturer):
                        devices[platform][manufacturer] = []

                    # Add new device to the list.
                    if not case_insensitive_in(self,
                                               devices[platform][manufacturer],
                                               device):
                        devices[platform][manufacturer].append(device)
            except csv.Error, e:
                sys.exit('file %s, line %d: %s'
                         % (filename, reader.line_num, e))

        # Sort manufacturers lists and device lists
        for platform in devices:
            # The manufacturers list doesn't exist if no devices exist
            # for the platform, so don't try to sort a non-existent
            # list.
            if 'manufacturers' in devices[platform]:
                devices[platform]['manufacturers'].sort()

            for manufacturer in devices[platform]:
                devices[platform][manufacturer].sort()

        if cacheDevices is True:
            cache.set('devices', devices, 600)

    return devices