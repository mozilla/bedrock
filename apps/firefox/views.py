import l10n_utils

def windows_billboards(req):
    major_version = req.GET.get('majorVersion')
    minor_version = req.GET.get('minorVersion')

    if major_version and minor_version:
        major_version = float(major_version)
        minor_version = float(minor_version)
        if major_version == 5 and minor_version == 1:
            return l10n_utils.render(req, 'firefox/unsupported-winxp.html')
    return l10n_utils.render(req, 'firefox/unsupported-win2k.html')

from django.core.files import File
import csv
from operator import itemgetter
import settings
import jinja2
import jingo

@jingo.register.function
@jinja2.contextfunction
def platforms(self):
    #list of supported platforms. Change this if the csv should define the
    #platforms
    return ['Phone', 'Tablet']

@jingo.register.function
@jinja2.contextfunction
def manufacturers(self, platform):
    supported_devices = loadDevices(self, platform)
    return sorted(supported_devices, key=itemgetter(0))

@jingo.register.function
@jinja2.contextfunction
def devices(self, platform, manufacturer):
    supported_devices = loadDevices(self, platform)
    if manufacturer in supported_devices:
        return supported_devices[manufacturer]
    else:
        return ['No Supported Devices']

@jingo.register.function
@jinja2.contextfunction
def loadDevices(self, platform):
    devices = dict()
    with open(settings.MEDIA_ROOT + '/devices.csv', 'rb') as file:
        # TODO: clean up fieldnames and handle whitespace better.
        # perhaps also case insensitivity, at least on platforms?
        #fieldnames = 'manufacturer','device', 'platform';
        reader = csv.DictReader(file, delimiter=',')
        try:
            for row in reader:
                if row[' platform'].lower() == platform.lower():
                    if row['manufacturer'] in devices:
                        devices[row['manufacturer']].append(row[' device'])
                    else:
                        devices[row['manufacturer']] = [row[' device']]
                else:
                    pass
        except csv.Error, e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    for manufacturer in devices:
        devices[manufacturer].sort()

    return devices
