# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.conf.urls import url
from django.shortcuts import render as django_render
from django.views.decorators.csrf import csrf_exempt

import basket
import fxa.constants
import fxa.errors
import fxa.oauth
import fxa.profile

import tweepy
import commonware.log
from lib import l10n_utils

try:
    import newrelic.agent
except ImportError:
    newrelic = False


log = commonware.log.getLogger('mozorg.util')

FXA_CLIENTS = {
    'oauth': None,
    'profile': None,
}


def page(name, tmpl, decorators=None, url_name=None, ftl_files=None, **kwargs):
    """
    Define a bedrock page.

    The URL name is the template name, with the extension stripped and the
    slashes changed to dots. So if tmpl="path/to/template.html", then the
    page's URL name will be "path.to.template". Set the `url_name` parameter
    to override this name.

    @param name: The URL regex pattern.  If not empty, a trailing slash is
        added automatically, so it shouldn't be included in the parameter
        value.
    @param tmpl: The template name.  Also used to come up with the URL name.
    @param decorators: A decorator or an iterable of decorators that should
        be applied to the view.
    @param url_name: The value to use as the URL name, default is to coerce
        the template path into a name as described above.
    @param active_locales: A list of locale codes that should be active for this page
        regardless of the state of the lang files. Useful for pages with locale-
        specific templates or non-English text in the template. Ignores the lang
        file activation tags.
    @param add_active_locales: A list of locale codes that should be active for this page
        in addition to those from the lang or ftl files.
    @param ftl_files: A list of FTL files that combined contain the strings for this page.
    @param kwargs: Any additional arguments are passed to l10n_utils.render
        as the context.
    """
    pattern = r'^%s/$' % name if name else r'^$'

    if url_name is None:
        # Set the name of the view to the template path replaced with dots
        (base, ext) = os.path.splitext(tmpl)
        url_name = base.replace('/', '.')

    # we don't have a caching backend yet, so no csrf (it's just a
    # newsletter form anyway)
    @csrf_exempt
    def _view(request):
        if newrelic:
            # Name this in New Relic to differentiate pages
            newrelic.agent.set_transaction_name(
                'mozorg.util.page:' + url_name.replace('.', '_'))
        kwargs.setdefault('urlname', url_name)

        # skip l10n if path exempt
        name_prefix = request.path_info.split('/', 2)[1]
        if name_prefix in settings.SUPPORTED_NONLOCALES:
            return django_render(request, tmpl, kwargs)

        return l10n_utils.render(request, tmpl, kwargs, ftl_files=ftl_files)

    # This is for graphite so that we can differentiate pages
    _view.page_name = url_name

    # Apply decorators
    if decorators:
        if callable(decorators):
            _view = decorators(_view)
        else:
            try:
                # Decorators should be applied in reverse order so that input
                # can be sent in the order your would write nested decorators
                # e.g. dec1(dec2(_view)) -> [dec1, dec2]
                for decorator in reversed(decorators):
                    _view = decorator(_view)
            except TypeError:
                log.exception('decorators not iterable or does not contain '
                              'callable items')

    return url(pattern, _view, name=url_name)


def get_fb_like_locale(request_locale):
    """
    Returns the most appropriate locale from the list of supported Facebook
    Like button locales. This can either be the locale itself if it's
    supported, the next matching locale for that language if any or failing
    any of that the default `en_US`.
    Ref: https://www.facebook.com/translations/FacebookLocales.xml

    Adapted from the facebookapp get_best_locale() util
    """

    lang = request_locale.replace('-', '_')

    if lang not in settings.FACEBOOK_LIKE_LOCALES:
        lang_prefix = lang.split('_')[0]

        try:
            lang = next(locale for locale in settings.FACEBOOK_LIKE_LOCALES
                        if locale.startswith(lang_prefix))
        except StopIteration:
            lang = 'en_US'

    return lang


def TwitterAPI():
    """
    Connect to the Twitter REST API using the Tweepy library.

    https://dev.twitter.com/docs/api/1.1
    http://pythonhosted.org/tweepy/html/
    """
    keys = settings.TWITTER_APP_KEYS
    if keys['consumer_key']:
        auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
        auth.set_access_token(keys['access_token'], keys['access_token_secret'])
        return tweepy.API(auth)
    else:
        return None


def get_tweets(account):
    """Return a list of twitter status objects for an account.

    :param account: twitter account to retrieve.
    :returns: list of Status objects or None on error.
    """
    # API Docs https://dev.twitter.com/rest/reference/get/statuses/user_timeline
    api = TwitterAPI()
    if api is None:
        return None

    account_opts = {
        'screen_name': account,
        'include_rts': True,
        'exclude_replies': True,
        # set this high because replies are excluded
        # after count is retrieved.
        'count': 100,
    }
    account_opts.update(settings.TWITTER_ACCOUNT_OPTS.get(account, {}))
    try:
        return api.user_timeline(**account_opts)
    except Exception:
        return None


def get_fxa_clients():
    """Return and/or create FxA OAuth client instances"""
    if FXA_CLIENTS['oauth'] is None:
        server_urls = fxa.constants.ENVIRONMENT_URLS.get(settings.FXA_OAUTH_SERVER_ENV)
        FXA_CLIENTS['oauth'] = fxa.oauth.Client(server_url=server_urls['oauth'])
        FXA_CLIENTS['profile'] = fxa.profile.Client(server_url=server_urls['profile'])

    return FXA_CLIENTS['oauth'], FXA_CLIENTS['profile']


def get_fxa_oauth_token(code):
    """Trade a one-time code for a longer use FxA OAuth token"""
    oauthClient, _ = get_fxa_clients()

    try:
        token_resp = oauthClient.trade_code(code, client_id=settings.FXA_OAUTH_CLIENT_ID, client_secret=settings.FXA_OAUTH_CLIENT_SECRET)
        token = token_resp['access_token']
    except Exception:
        token = None

    return token


def get_fxa_profile_email(token):
    """Retrieve the email address associated with an FxA OAuth token"""
    _, profileClient = get_fxa_clients()

    try:
        email = profileClient.get_email(token)
    except Exception:
        email = None

    return email


def fxa_concert_rsvp(email, isFx):
    data = {
        'email': email,
        'is_firefox': 'Y' if isFx else 'N',
        'campaign_id': 'firefox-concert-series-Q4-2018',  # or something. just here in case there's another of these some day.
        'api_key': settings.BASKET_API_KEY,
    }

    try:
        basket.request('post', 'fxa-concerts-rsvp', data=data)
        return True
    except Exception:
        return False
