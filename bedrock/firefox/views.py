# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re
from cgi import escape

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_headers
from django.views.generic.base import TemplateView

import basket
from bedrock.base.helpers import static
from bedrock.base.urlresolvers import reverse
from lib import l10n_utils
from lib.l10n_utils.dotlang import _
from product_details.version_compare import Version
import waffle

from bedrock.base.geo import get_country_from_request
from bedrock.firefox.firefox_details import firefox_desktop
from bedrock.firefox.forms import SMSSendForm, SendToDeviceWidgetForm
from bedrock.mozorg.views import process_partnership_form
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.releasenotes import version_re


UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

LANG_FILES = ['firefox/partners/index']

LOCALE_FXOS_HEADLINES = {
    'de': {
        'title': u"Firefox OS ist richtungsweisend für die Zukunft des "
                 u"mobilen Marktes",
        'url': 'http://blog.mozilla.org/press-de/2014/02/23/'
               'firefox-os-ist-richtungsweisend-fur-die-zukunft-des-mobilen-'
               'marktes',
    },
    'en-GB': {
        'title': u'Firefox OS Unleashes the Future of Mobile',
        'url': 'http://blog.mozilla.org/press-uk/2014/02/23/'
               'firefox-os-unleashes-the-future-of-mobile'
    },
    'en-US': {
        'title': _('Firefox OS Unleashes the Future of Mobile'),
        'url': 'https://blog.mozilla.org/press/2014/02/firefox-os-future-2/',
    },
    'es-AR': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'http://blog.mozilla.org/press-latam/2014/02/23/'
               'firefox-os-te-desvela-el-futuro-de-lo-movil/',
    },
    'es-CL': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'http://blog.mozilla.org/press-latam/2014/02/23/'
               'firefox-os-te-desvela-el-futuro-de-lo-movil/',
    },
    'es-ES': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'https://blog.mozilla.org/press/2014/02/firefox-os-future-2/',
    },
    'es-MX': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'http://blog.mozilla.org/press-latam/2014/02/23/'
               'firefox-os-te-desvela-el-futuro-de-lo-movil/',
    },
    'fr': {
        'title': u'Firefox OS chamboule le futur du mobile',
        'url': 'http://blog.mozilla.org/press-fr/2014/02/23/'
               'firefox-os-chamboule-le-futur-du-mobile',
    },
    'it': {
        'title': u'Firefox OS svela il futuro del mobile',
        'url': 'http://blog.mozilla.org/press-it/2014/02/23/'
               'firefox-os-svela-il-futuro-del-mobile',
    },
    'pl': {
        'title': u'Firefox OS uwalnia przyszłość technologii mobilnej',
        'url': 'http://blog.mozilla.org/press-pl/2014/02/23/'
               'firefox-os-uwalnia-przyszlosc-technologii-mobilnej',
    },
    'pt-BR': {
        'title': u'Firefox OS apresenta o futuro dos dispositivos móveis',
        'url': 'https://blog.mozilla.org/press-br/2014/02/23/'
               'firefox-os-apresenta-o-futuro-dos-dispositivos-moveis/',
    },
}

INSTALLER_CHANNElS = [
    'release',
    'beta',
    'alpha',
    # 'nightly',  # soon
]

SMS_MESSAGES = {
    'android': 'SMS_Android',
    'android-test-modal': 'android-download-notembed',  # test variant
    'android-test-embed': 'android-download-embed',  # test variant
}

EMAIL_MESSAGES = {
    'android': 'download-firefox-android',
    'android-test-modal': 'get-android-notembed',  # test variant
    'android-test-embed': 'get-android-embed',  # test variant
    'ios': 'download-firefox-ios',
    'all': 'download-firefox-mobile',
}

LOCALE_SPRING_CAMPAIGN_VIDEOS = {
    'en-US': 'https://videos.cdn.mozilla.net/uploads/marketing/SpringCampaign2015/Firefox_Welcome_english',
    'en-GB': 'https://videos.cdn.mozilla.net/uploads/marketing/SpringCampaign2015/Firefox_Welcome_englishUK',
    'de': 'https://videos.cdn.mozilla.net/uploads/marketing/SpringCampaign2015/Firefox_Welcome_german',
    'es-ES': 'https://videos.cdn.mozilla.net/uploads/marketing/SpringCampaign2015/Firefox_Welcome_spanish',
    'es-MX': 'https://videos.cdn.mozilla.net/uploads/marketing/SpringCampaign2015/Firefox_Welcome_spanishMX',
    'fr': 'https://videos.cdn.mozilla.net/uploads/marketing/SpringCampaign2015/Firefox_Welcome_french',
    'pt-BR': 'https://videos.cdn.mozilla.net/uploads/marketing/SpringCampaign2015/Firefox_Welcome_portugeseBrazil',
}


def get_js_bundle_files(bundle):
    """
    Return a JSON string of the list of file names for lazy loaded
    javascript.
    """
    bundle = settings.PIPELINE_JS[bundle]
    if settings.DEBUG:
        items = bundle['source_filenames']
    else:
        items = (bundle['output_filename'],)
    return json.dumps([static(i) for i in items])


JS_COMMON = get_js_bundle_files('partners_common')
JS_MOBILE = get_js_bundle_files('partners_mobile')
JS_DESKTOP = get_js_bundle_files('partners_desktop')


def installer_help(request):
    installer_lang = request.GET.get('installer_lang', None)
    installer_channel = request.GET.get('channel', None)
    context = {
        'installer_lang': None,
        'installer_channel': None,
    }

    if installer_lang and installer_lang in firefox_desktop.languages:
        context['installer_lang'] = installer_lang

    if installer_channel and installer_channel in INSTALLER_CHANNElS:
        context['installer_channel'] = installer_channel

    return l10n_utils.render(request, 'firefox/installer-help.html', context)


@csrf_exempt
def sms_send(request):
    form = SMSSendForm(request.POST or None)
    if request.method == 'POST':
        error_msg = _('An error occurred in our system. Please try again later.')
        error = None
        if form.is_valid():
            try:
                basket.send_sms(form.cleaned_data['number'],
                                SMS_MESSAGES['android'],
                                form.cleaned_data['optin'])
            except basket.BasketException:
                error = error_msg

        else:
            number_errors = form.errors.get('number')
            if number_errors:
                # form error messages may contain unsanitized user input
                error = escape(number_errors[0])
            else:
                error = error_msg

        if request.is_ajax():
            # return JSON
            if error:
                resp = {
                    'success': False,
                    'error': error,
                }
            else:
                resp = {'success': True}

            return HttpResponseJSON(resp)
        else:
            if error:
                form.errors['__all__'] = form.error_class([error])
            else:
                return HttpResponseRedirect(reverse('firefox.android.sms-thankyou'))

    return l10n_utils.render(request, 'firefox/android/sms-send.html',
                             {'sms_form': form})


@require_POST
@csrf_exempt
def send_to_device_ajax(request):
    locale = l10n_utils.get_locale(request)
    phone_or_email = request.POST.get('phone-or-email')
    if not phone_or_email:
        return HttpResponseJSON({'success': False, 'errors': ['phone-or-email']})

    data = {
        'platform': request.POST.get('platform'),
    }

    data_type = 'email' if '@' in phone_or_email else 'number'
    data[data_type] = phone_or_email
    form = SendToDeviceWidgetForm(data)

    if form.is_valid():
        phone_or_email = form.cleaned_data.get(data_type)
        platform = form.cleaned_data.get('platform')

        # check for android & valid send to device test value
        # update email/sms message if conditions match
        send_to_device_test = request.POST.get('android-send-to-device-test')
        if (platform == 'android' and send_to_device_test in
                ['android-test-modal', 'android-test-embed']):

            platform = send_to_device_test

        if data_type == 'number':
            if platform in SMS_MESSAGES:
                try:
                    basket.send_sms(phone_or_email, SMS_MESSAGES[platform])
                except basket.BasketException:
                    return HttpResponseJSON({'success': False, 'errors': ['system']},
                                            status=400)
            else:
                # TODO define all platforms in SMS_MESSAGES
                return HttpResponseJSON({'success': False, 'errors': ['platform']})
        else:  # email
            if platform in EMAIL_MESSAGES:
                try:
                    basket.subscribe(phone_or_email, EMAIL_MESSAGES[platform],
                                     source_url=request.POST.get('source-url'),
                                     lang=locale)
                except basket.BasketException:
                    return HttpResponseJSON({'success': False, 'errors': ['system']},
                                            status=400)
            else:
                # TODO define all platforms in EMAIL_MESSAGES
                return HttpResponseJSON({'success': False, 'errors': ['platform']})

        resp_data = {'success': True}
    else:
        resp_data = {
            'success': False,
            'errors': form.errors.keys(),
        }

    return HttpResponseJSON(resp_data)


def windows_billboards(req):
    major_version = req.GET.get('majorVersion')
    minor_version = req.GET.get('minorVersion')

    if major_version and minor_version:
        major_version = float(major_version)
        minor_version = float(minor_version)
        if major_version == 5 and minor_version == 1:
            return l10n_utils.render(req, 'firefox/unsupported/winxp.html')
    return l10n_utils.render(req, 'firefox/unsupported/win2k.html')


def fx_home_redirect(request):
    return HttpResponseRedirect(reverse('firefox.new'))


def dnt(request):
    response = l10n_utils.render(request, 'firefox/dnt.html')
    response['Vary'] = 'DNT'
    return response


def all_downloads(request, channel):
    if channel is None:
        channel = 'release'
    if channel == 'developer':
        channel = 'alpha'
    if channel == 'organizations':
        channel = 'esr'

    version = firefox_desktop.latest_version(channel)
    query = request.GET.get('q')

    channel_names = {
        'release': _('Firefox'),
        'beta': _('Firefox Beta'),
        'alpha': _('Developer Edition'),
        'esr': _('Firefox Extended Support Release'),
    }

    context = {
        'full_builds_version': version.split('.', 1)[0],
        'full_builds': firefox_desktop.get_filtered_full_builds(channel, version, query),
        'test_builds': firefox_desktop.get_filtered_test_builds(channel, version, query),
        'query': query,
        'channel': channel,
        'channel_name': channel_names[channel]
    }

    if channel == 'esr':
        next_version = firefox_desktop.latest_version('esr_next')
        if next_version:
            context['full_builds_next_version'] = next_version.split('.', 1)[0]
            context['full_builds_next'] = firefox_desktop.get_filtered_full_builds('esr_next',
                                                                                   next_version, query)
            context['test_builds_next'] = firefox_desktop.get_filtered_test_builds('esr_next',
                                                                                   next_version, query)
    return l10n_utils.render(request, 'firefox/all.html', context)


@never_cache
def firefox_os_geo_redirect(request):
    country = get_country_from_request(request)
    version = settings.FIREFOX_OS_COUNTRY_VERSIONS.get(
        country,
        settings.FIREFOX_OS_COUNTRY_VERSIONS['default']
    )

    return HttpResponseRedirect(reverse('firefox.os.ver.{0}'.format(version)))


@csrf_protect
def firefox_partners(request):
    # If the current locale isn't in our list, return the en-US value
    press_locale = request.locale if (
        request.locale in LOCALE_FXOS_HEADLINES) else 'en-US'

    template_vars = {
        'locale_headline_url': LOCALE_FXOS_HEADLINES[press_locale]['url'],
        'locale_headline_title': LOCALE_FXOS_HEADLINES[press_locale]['title'],
        'js_common': JS_COMMON,
        'js_mobile': JS_MOBILE,
        'js_desktop': JS_DESKTOP,
    }

    form_kwargs = {
        'interest_set': 'fx',
        'lead_source': 'www.mozilla.org/firefox/partners/'}

    return process_partnership_form(
        request, 'firefox/partners/index.html', 'firefox.partners.index', template_vars, form_kwargs)


def show_devbrowser_firstrun_or_whatsnew(version):
    match = re.match(r'\d{1,2}', version)
    if match:
        num_version = int(match.group(0))
        return num_version >= 35 and version.endswith('a2')

    return False


def show_search_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('34.0')


def show_36_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('36.0')


def show_36_whatsnew_tour(oldversion):
    try:
        oldversion = Version(oldversion)
    except ValueError:
        return False

    return oldversion < Version('36.0')


def show_38_0_5_firstrun_or_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('38.0.5')


def show_40_firstrun(version):
    if (waffle.switch_is_active('fx40-firstrun')):
        try:
            version = Version(version)
        except ValueError:
            return False

        return version >= Version('40.0')
    else:
        return False


class LatestFxView(TemplateView):

    """
    Base class to be extended by views that require visitor to be
    using latest version of Firefox. Classes extending this class must
    implement either `get_template_names` function or provide
    `template_name` class attribute. Control where to redirect non
    Firefox users by setting the `non_fx_redirect` attribute to
    a url name.
    """
    non_fx_redirect = 'firefox.new'

    @vary_on_headers('User-Agent')
    def dispatch(self, *args, **kwargs):
        return super(LatestFxView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # required for newsletter form post that is handled in
        # newsletter/helpers.py
        return self.get(request, *args, **kwargs)

    def redirect_to(self):
        """
        Redirect visitors based on their user-agent.

        - Up-to-date Firefox users pass through.
        - Other Firefox users go to the new page.
        - Non Firefox users go to the configured page.
        """
        query = self.request.META.get('QUERY_STRING')
        query = '?' + query if query else ''

        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        if 'Firefox' not in user_agent:
            return reverse(self.non_fx_redirect) + query
            # TODO : Where to redirect bug 757206

        return None

    def render_to_response(self, context, **response_kwargs):
        redirect_url = self.redirect_to()

        if redirect_url is not None:
            return HttpResponsePermanentRedirect(redirect_url)
        else:
            return l10n_utils.render(self.request,
                                     self.get_template_names(),
                                     context,
                                     **response_kwargs)


class FirstrunView(LatestFxView):

    def get(self, request, *args, **kwargs):
        if not settings.DEV and not request.is_secure():
            uri = 'https://{host}{path}'.format(
                host=request.get_host(),
                path=request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(uri)
        return super(FirstrunView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(FirstrunView, self).get_context_data(**kwargs)

        version = self.kwargs.get('version') or ''

        # add version to context for use in templates
        ctx['version'] = version

        return ctx

    def get_template_names(self):
        version = self.kwargs.get('version') or ''
        locale = l10n_utils.get_locale(self.request)

        if show_devbrowser_firstrun_or_whatsnew(version):
            template = 'firefox/dev-firstrun.html'
        elif show_40_firstrun(version):
            template = 'firefox/australis/fx40/firstrun.html'
        elif show_38_0_5_firstrun_or_whatsnew(version):
            template = 'firefox/australis/fx38_0_5/firstrun.html'
        elif show_36_firstrun(version):
            template = 'firefox/australis/fx36/firstrun-tour.html'
        elif show_search_firstrun(version) and locale == 'en-US':
            template = 'firefox/australis/firstrun-34-tour.html'
        else:
            template = 'firefox/australis/firstrun-tour.html'

        # return a list to conform with original intention
        return [template]


class WhatsnewView(LatestFxView):

    pocket_locales = ['en-US', 'es-ES', 'ru', 'ja', 'de']

    def get(self, request, *args, **kwargs):
        if not settings.DEV and not request.is_secure():
            uri = 'https://{host}{path}'.format(
                host=request.get_host(),
                path=request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(uri)
        return super(WhatsnewView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(WhatsnewView, self).get_context_data(**kwargs)
        locale = l10n_utils.get_locale(self.request)
        video_url = LOCALE_SPRING_CAMPAIGN_VIDEOS.get(locale, False)

        if video_url:
            ctx['video_url'] = video_url

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        version = self.kwargs.get('version') or ''
        oldversion = self.request.GET.get('oldversion', '')
        # old versions of Firefox sent a prefixed version
        if oldversion.startswith('rv:'):
            oldversion = oldversion[3:]

        if show_devbrowser_firstrun_or_whatsnew(version):
            template = 'firefox/dev-whatsnew.html'
        elif show_38_0_5_firstrun_or_whatsnew(version):
            has_video = LOCALE_SPRING_CAMPAIGN_VIDEOS.get(locale, False)
            has_pocket = locale in self.pocket_locales
            if has_pocket and has_video:
                template = 'firefox/whatsnew_38/whatsnew-pocket-video.html'
            elif has_video:
                template = 'firefox/whatsnew_38/whatsnew-video.html'
            elif has_pocket:
                template = 'firefox/whatsnew_38/whatsnew-pocket.html'
            else:
                template = 'firefox/australis/fx36/whatsnew-no-tour.html'
        elif version.startswith('37.'):
            template = 'firefox/whatsnew-fx37.html'
        elif version.startswith('36.'):
            if show_36_whatsnew_tour(oldversion):
                template = 'firefox/australis/fx36/whatsnew-tour.html'
            else:
                template = 'firefox/australis/fx36/whatsnew-no-tour.html'
        else:
            template = 'firefox/australis/whatsnew-no-tour.html'

        # return a list to conform with original intention
        return [template]


class TourView(LatestFxView):

    def get(self, request, *args, **kwargs):
        if not settings.DEV and not request.is_secure():
            uri = 'https://{host}{path}'.format(
                host=request.get_host(),
                path=request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(uri)
        return super(TourView, self).get(request, *args, **kwargs)

    def get_template_names(self):
        version = self.kwargs.get('version') or ''
        locale = l10n_utils.get_locale(self.request)

        if show_devbrowser_firstrun_or_whatsnew(version):
            template = 'firefox/dev-firstrun.html'
        elif show_36_firstrun(version):
            template = 'firefox/australis/fx36/help-menu-36-tour.html'
        elif show_search_firstrun(version) and locale == 'en-US':
            template = 'firefox/australis/help-menu-34-tour.html'
        else:
            template = 'firefox/australis/help-menu-tour.html'

        # return a list to conform with original intention
        return [template]


def hello(request):
    videos = {
        'ar': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_arabic',
        'de': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_german',
        'en-US': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_english',
        'es-AR': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_spanish',
        'es-CL': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_spanish',
        'es-ES': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_spanish',
        'es-MX': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_spanish',
        'fr': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_french',
        'id': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_indonesian',
        'it': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_italian',
        'ja': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_japanese',
        'pl': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_polish',
        'pt-BR': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_portugese',
        'ru': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_russian',
        'tr': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_turkish',
        'zh-TW': 'https://videos.cdn.mozilla.net/uploads/FirefoxHello/firefoxhello_intro_chinese'
    }

    return l10n_utils.render(request, 'firefox/hello/index.html',
        {'video_url': videos.get(request.locale, videos.get('en-US'))})


class HelloStartView(LatestFxView):
    non_fx_redirect = 'firefox.hello'
    template_name = 'firefox/hello/start.html'


class FeedbackView(TemplateView):

    def get_template_names(self):
        score = self.request.GET.get('score', 0)
        if score > '3':
            template = 'firefox/feedback/happy.html'
        else:
            template = 'firefox/feedback/unhappy.html'

        return [template]


def android(request):
    # check for variant in querystring for send-to-device testing
    variant = request.GET.get('v', '')

    # ensure variant is one of 3 accepted values
    if (variant not in ['a', 'b', 'c']):
        variant = ''

    return l10n_utils.render(request, 'firefox/android/index.html',
        {'variant': variant})


class TrackingProtectionTourView(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'firefox/tracking-protection-tour.html'
