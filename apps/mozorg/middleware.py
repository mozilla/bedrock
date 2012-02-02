from email.utils import formatdate
import datetime
from time import mktime

class CacheMiddleware(object):

    def process_response(self, request, response):
        if response.status_code != 404 and 'Cache-Control' not in response:
            d = datetime.datetime.now() + datetime.timedelta(minutes=10)
            stamp = mktime(d.timetuple())

            response['Cache-Control'] = 'max-age=600'
            response['Expires'] = formatdate(timeval=stamp, localtime=False, usegmt=True)
        return response
