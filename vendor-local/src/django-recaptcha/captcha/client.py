import urllib
import urllib2

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.utils.safestring import mark_safe

DEFAULT_API_SSL_SERVER = "https://www.google.com/recaptcha/api"
DEFAULT_API_SERVER = "http://www.google.com/recaptcha/api"
DEFAULT_VERIFY_SERVER = "www.google.com"
DEFAULT_WIDGET_TEMPLATE = 'captcha/widget.html'

API_SSL_SERVER = getattr(settings, "CAPTCHA_API_SSL_SERVER", \
        DEFAULT_API_SSL_SERVER)
API_SERVER = getattr(settings, "CAPTCHA_API_SERVER", DEFAULT_API_SERVER)
VERIFY_SERVER = getattr(settings, "CAPTCHA_VERIFY_SERVER", \
        DEFAULT_VERIFY_SERVER)
WIDGET_TEMPLATE = getattr(settings, "CAPTCHA_WIDGET_TEMPLATE", \
        DEFAULT_WIDGET_TEMPLATE)


RECAPTCHA_SUPPORTED_LANUAGES = ('en', 'nl', 'fr', 'de', 'pt', 'ru', 'es', 'tr')


class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code


def displayhtml(public_key,
    attrs,
    use_ssl=False,
    error=None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    if not 'lang' in attrs:
        attrs['lang'] = settings.LANGUAGE_CODE[:2]

    return render_to_string(WIDGET_TEMPLATE,
            {'api_server': server,
             'public_key': public_key,
             'error_param': error_param,
             'options': mark_safe(json.dumps(attrs, indent=2))
             })


def submit(recaptcha_challenge_field,
    recaptcha_response_field,
    private_key,
    remoteip,
    use_ssl=False):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field
    from the form
    recaptcha_response_field -- The value of recaptcha_response_field
    from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len(recaptcha_response_field) and len(recaptcha_challenge_field)):
        return RecaptchaResponse(
            is_valid=False,
            error_code='incorrect-captcha-sol'
        )

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode({
            'privatekey': encode_if_necessary(private_key),
            'remoteip':  encode_if_necessary(remoteip),
            'challenge':  encode_if_necessary(recaptcha_challenge_field),
            'response':  encode_if_necessary(recaptcha_response_field),
            })

    if use_ssl:
        verify_url = 'https://%s/recaptcha/api/verify' % VERIFY_SERVER
    else:
        verify_url = 'http://%s/recaptcha/api/verify' % VERIFY_SERVER

    request = urllib2.Request(
        url=verify_url,
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )

    httpresp = urllib2.urlopen(request)

    return_values = httpresp.read().splitlines()
    httpresp.close()

    return_code = return_values[0]

    if (return_code == "true"):
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(is_valid=False, error_code=return_values[1])
