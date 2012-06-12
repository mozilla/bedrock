import l10n_utils
import csv
from operator import itemgetter

from django.core.files import File
from django.core.cache import cache

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
    return l10n_utils.render(request, 'firefox/mobile/platforms.html', {'devices': load_devices(request)} )

def load_devices(self):
    devices = cache.get('devices')
    if devices is None:
        #List of supported platforms. Any row in the csv that doesn't match one
        #of these platforms will be ignored. Change this if the csv should
        #define the platforms.
        platforms = ['Phone', 'Tablet']
        devices = dict()
        for platform in platforms:
            devices[platform] = dict()

        with open(settings.MEDIA_ROOT + '/devices.csv', 'rb') as file:
            reader = csv.DictReader(
                file,
                fieldnames = ('manufacturer','device', 'platform'),
                delimiter = ',',
                skipinitialspace = True
            )

            # skip header row
            next(reader)

            try:
                for row in reader:
                    platform = row['platform'].strip()
                    if platform in devices:
                        #strip leading and trailing whitespace
                        manufacturer = row['manufacturer'].strip()
                        device = row['device'].strip()
                        if manufacturer in devices[platform]:
                            devices[platform][manufacturer].append(device)
                        else:
                            devices[platform][manufacturer] = [device]
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

        for platform in devices:
            #TODO -how to get manufacturers returned as the correct order
            #manufacturers = sorted(devices[platform], key=itemgetter(0))
            for manufacturer in devices[platform]:
                devices[platform][manufacturer].sort()

        cache.set('devices', devices, 600)
    return devices

def dnt(request):
    response = l10n_utils.render(request, 'firefox/dnt.html')
    response['Vary'] = 'DNT'
    return response
