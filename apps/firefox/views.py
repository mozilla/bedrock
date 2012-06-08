import l10n_utils
import csv
from operator import itemgetter

from django.core.files import File
from django.core.cache import cache
import jinja2
import jingo

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

@jingo.register.function
@jinja2.contextfunction
def platforms(self):
    #list of supported platforms. Change this if the csv should define the
    #platforms
    return ['Phone', 'Tablet']

@jingo.register.function
@jinja2.contextfunction
def manufacturers(self, platform):
    supported_devices = load_devices(self, platform)
    return sorted(supported_devices, key=itemgetter(0))

@jingo.register.function
@jinja2.contextfunction
def devices(self, platform, manufacturer):
    supported_devices = load_devices(self, platform)
    if manufacturer in supported_devices:
        return supported_devices[manufacturer]
    else:
        return ['No Supported Devices']

def load_devices(self, platform):
    devices = cache.get('devices')
    if devices is None:
        devices = dict()
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
                    if row['platform'].lower() == platform.lower():
                        #strip leading and trailing whitespace
                        manufacturer = row['manufacturer'].strip()
                        device = row['device'].strip()
                        if manufacturer in devices:
                            devices[manufacturer].append(device)
                        else:
                            devices[manufacturer] = [device]
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

        for manufacturer in devices:
            devices[manufacturer].sort()

        cache.set('devices', devices, 600)

    return devices