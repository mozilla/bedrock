import csv
import l10n_utils
from operator import itemgetter

from django.core.cache import cache
from django.core.files import File

from django.conf import settings

def windows_billboards(req):
    major_version = req.GET.get('majorVersion')
    minor_version = req.GET.get('minorVersion')

    if major_version and minor_version:
        major_version = float(major_version)
        minor_version = float(minor_version)
        if major_version == 5 and minor_version == 1:
            return l10n_utils.render(req, 'firefox/unsupported-winxp.html')
    return l10n_utils.render(req, 'firefox/unsupported-win2k.html')

def platforms(request):
    return l10n_utils.render(
        request,
        'firefox/mobile/platforms.html',
        {'devices': load_devices(request, settings.MEDIA_ROOT + '/devices.csv')}
    )

def case_insensitive_in(self, list, value):
    #used in load_devices to lookup existing platform/manufacturer/device
    #combinations in a case insensitive manner. This prevents duplicates from
    #being displayed if they are entered twice by accident with different
    #capitalization. If this happens, capitalization from the first instance
    #will be used.
    for i in list:
        if value.lower() == i.lower():
            return True

    return False

def load_devices(self, file, cacheDevices = True):
    devices = None
    if cacheDevices is True:
        devices = cache.get('devices')

    if devices is None:
        #List of supported platforms. Any row in the csv that doesn't match one
        #of these platforms will be ignored. Change this if the csv should
        #define the platforms.
        platforms = ['Phone', 'Tablet']
        devices = dict()
        for platform in platforms:
            devices[platform] = dict()

        with open(file, 'rb') as file:
            reader = csv.DictReader(
                file,
                delimiter = ',',
                skipinitialspace = True
            )

            #strip leading and trailing whitespace from each value to normalize
            #values in the csv. This prevents whitespace from creating double
            #entries for any platform/manufacturer/device combination.
            reader = (
                dict((k, v.strip()) for k, v in row.items())
                for row in reader
            )

            try:
                for row in reader:
                    #local variables for code readability
                    platform = row['platform']
                    manufacturer = row['manufacturer']
                    device = row['device']

                    if not case_insensitive_in(self, devices, platform):
                        continue

                    #store the manufacturers in a list so they can easily be
                    #access after being sorted. init the list when its a new
                    #platform
                    if 'manufacturers' not in devices[platform]:
                        devices[platform]['manufacturers'] = []

                    #add new manufacturers to the list
                    if not case_insensitive_in(
                        self,
                        devices[platform]['manufacturers'],
                        manufacturer
                    ):
                        devices[platform]['manufacturers'].append(manufacturer)

                    # init the list of devices for new manufacturer
                    if not case_insensitive_in(
                        self,
                        devices[platform],
                        manufacturer
                    ):
                        devices[platform][manufacturer] = []

                    #store device names in a nested dict by platform and
                    #manufacturer
                    if not case_insensitive_in(
                        self,
                        devices[platform][manufacturer],
                        device
                    ):
                        devices[platform][manufacturer].append(device)
            except csv.Error, e:
                sys.exit(
                    'file %s, line %d: %s' % (filename, reader.line_num, e)
                )

        #sort manufacturers lists and device lists
        for platform in devices:
            devices[platform]['manufacturers'].sort()
            for manufacturer in devices[platform]:
                devices[platform][manufacturer].sort()

        if cacheDevices is True:
            cache.set('devices', devices, 600)
    return devices

def dnt(request):
    response = l10n_utils.render(request, 'firefox/dnt.html')
    response['Vary'] = 'DNT'
    return response
