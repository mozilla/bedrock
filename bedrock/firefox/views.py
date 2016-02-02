# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.conf import settings
from django.http import (Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect)
from django.utils.encoding import force_text
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_headers
from django.views.generic.base import TemplateView

import basket
from bedrock.base.urlresolvers import reverse
from commonware.response.decorators import xframe_allow
from lib import l10n_utils
from product_details.version_compare import Version

import waffle

from bedrock.base.geo import get_country_from_request
from bedrock.firefox.firefox_details import firefox_desktop, firefox_android
from bedrock.firefox.forms import SendToDeviceWidgetForm
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.releasenotes import version_re


UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

INSTALLER_CHANNElS = [
    'release',
    'beta',
    'alpha',
    # 'nightly',  # soon
]

SMS_MESSAGES = {
    'ios': 'ff-ios-download',
    'android': 'SMS_Android',
    # /firefox/android page variant
    'android-embed': 'android-download-embed',
}

EMAIL_MESSAGES = {
    'android': 'download-firefox-android',
    # /firefox/android page variant
    'android-embed': 'get-android-embed',
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

        # check for customized widget and update email/sms
        # message if conditions match
        send_to_device_basket_id = request.POST.get('send-to-device-basket-id')
        if (platform == 'android' and
                send_to_device_basket_id == 'android-embed'):

            platform = 'android-embed'

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


def choose(request):
    if waffle.switch_is_active('tracking-protection-redirect'):
        return l10n_utils.render(request, 'firefox/choose.html')
    else:
        query = force_text(request.META.get('QUERY_STRING'), errors='ignore')
        return HttpResponseRedirect('?'.join([reverse('firefox.new'), query]))


def dnt(request):
    response = l10n_utils.render(request, 'firefox/dnt.html')
    response['Vary'] = 'DNT'
    return response


def all_downloads(request, platform, channel):
    if platform is None:
        platform = 'desktop'
    if platform == 'desktop':
        product = firefox_desktop
    if platform == 'android':
        product = firefox_android

    if channel is None:
        channel = 'release'
    if channel in ['developer', 'aurora']:
        channel = 'alpha'
    if channel == 'organizations':
        channel = 'esr'

    # Since the regex in urls.py matches various URL patterns, we have to handle
    # nonexistent pages here as 404 Not Found
    if platform == 'ios':
        raise Http404
    if platform == 'android' and channel in ['alpha', 'esr']:
        raise Http404

    version = product.latest_version(channel)
    query = request.GET.get('q')

    context = {
        'platform': platform,
        'platforms': product.platforms(channel),
        'full_builds_version': version.split('.', 1)[0],
        'full_builds': product.get_filtered_full_builds(channel, version, query),
        'test_builds': product.get_filtered_test_builds(channel, version, query),
        'query': query,
        'channel': channel,
        'channel_label': product.channel_labels.get(channel, 'Firefox'),
    }

    if platform == 'desktop' and channel == 'esr':
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
    locale = l10n_utils.get_locale(request)
    if locale == 'en-US':
        version = '2.5'
    else:
        country = get_country_from_request(request)
        version = settings.FIREFOX_OS_COUNTRY_VERSIONS.get(
            country,
            settings.FIREFOX_OS_COUNTRY_VERSIONS['default']
        )

    return HttpResponseRedirect(reverse('firefox.os.ver.{0}'.format(version)))


def show_devbrowser_firstrun_or_whatsnew(version):
    match = re.match(r'\d{1,2}', version)
    if match:
        num_version = int(match.group(0))
        return num_version >= 35 and version.endswith('a2')

    return False


def show_36_tour(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('36.0')


def show_38_0_5_firstrun_or_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('38.0.5')


def show_42_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('42.0')


def show_40_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('40.0')


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

    def get_context_data(self, **kwargs):
        ctx = super(FirstrunView, self).get_context_data(**kwargs)
        version = self.kwargs.get('version') or ''

        # add version to context for use in templates
        ctx['version'] = version

        return ctx

    def get_template_names(self):
        version = self.kwargs.get('version') or ''

        if show_devbrowser_firstrun_or_whatsnew(version):
            template = 'firefox/dev-firstrun.html'
        elif show_40_firstrun(version):
            template = 'firefox/firstrun/firstrun.html'
        elif show_38_0_5_firstrun_or_whatsnew(version):
            template = 'firefox/australis/fx38_0_5/firstrun.html'
        else:
            template = 'firefox/australis/firstrun.html'

        # return a list to conform with original intention
        return [template]


class FirstrunLearnMoreView(LatestFxView):
    template_name = 'firefox/whatsnew_42/learnmore.html'


class WhatsnewView(LatestFxView):

    pocket_locales = ['en-US', 'es-ES', 'ru', 'ja', 'de']

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
        elif show_42_whatsnew(version):
            template = 'firefox/whatsnew_42/whatsnew.html'
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
                template = 'firefox/australis/whatsnew.html'
        else:
            template = 'firefox/australis/whatsnew.html'

        # return a list to conform with original intention
        return [template]


class TourView(LatestFxView):

    def get_template_names(self):
        version = self.kwargs.get('version') or ''

        if show_devbrowser_firstrun_or_whatsnew(version):
            template = 'firefox/dev-firstrun.html'
        elif show_36_tour(version):
            template = 'firefox/australis/fx36/tour.html'
        else:
            template = 'firefox/australis/firstrun.html'

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

    if (waffle.switch_is_active('firefox-hello-2016')):
        return l10n_utils.render(request, 'firefox/hello/index-2016.html')
    else:
        return l10n_utils.render(request, 'firefox/hello/index.html',
        {'video_url': videos.get(request.locale, videos.get('en-US'))})


class HelloStartView(LatestFxView):
    non_fx_redirect = 'firefox.hello'
    template_name = 'firefox/hello/start.html'


class FeedbackView(TemplateView):

    donate_url = ('https://donate.mozilla.org/'
       '?ref=EOYFR2015&utm_campaign=EOYFR2015'
       '&utm_source=Heartbeat_survey&utm_medium=referral'
       '&utm_content=Heartbeat_{0}stars')

    def get_score(self):
        return self.request.GET.get('score', 0)

    def get_template_names(self):
        score = self.get_score()
        if score > '3':
            template = 'firefox/feedback/happy.html'
        else:
            template = 'firefox/feedback/unhappy.html'

        return [template]

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)
        score = self.get_score()

        if score in ['3', '4', '5']:
            context['donate_stars_url'] = self.donate_url.format(score)

        return context


class Win10Welcome(l10n_utils.LangFilesMixin, TemplateView):

    def get_template_names(self):
        # check for variant in querystring for multi-variant testing.
        v = self.request.GET.get('v', '')
        template = 'firefox/win10-welcome.html'

        # ensure variant is one of 4 accepted values and locale is en-US only.
        # now on round 3 of testing, hence "-3" in template name
        if (v in map(str, range(1, 11)) and self.request.locale == 'en-US'):
            template = 'firefox/win10_variants/variant-3-' + v + '.html'

        return [template]


class TrackingProtectionTourView(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'firefox/tracking-protection-tour.html'


@xframe_allow
def new(request):
    # Remove legacy query parameters (Bug 1236791)
    if request.GET.get('product', None) or request.GET.get('os', None):
        return HttpResponsePermanentRedirect(reverse('firefox.new'))

    return l10n_utils.render(request, 'firefox/new.html')
