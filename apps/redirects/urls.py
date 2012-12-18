# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls.defaults import *

from util import redirect


urlpatterns = patterns('',

    redirect(r'^b2g', 'firefoxos.firefoxos'),
    redirect(r'^b2g/faq', 'firefoxos.firefoxos'),
    redirect(r'^b2g/about', 'firefoxos.firefoxos'),

    redirect(r'^contribute/areas.html$', 'mozorg.contribute'),  # Bug 781914
    redirect(r'^projects/$', 'mozorg.products'),  # Bug 763665

    # Bug 792185 Brand Toolkit -> Style Guide
    redirect(r'^firefox/brand/$', 'styleguide.home'),
    redirect(r'^firefox/brand/platform/$', 'styleguide.identity.firefox-family-platform'),
    redirect(r'^firefox/brand/identity/$', 'styleguide.identity.firefox-branding'),
    redirect(r'^firefox/brand/identity/channel-logos/$', 'styleguide.identity.firefox-channels'),
    redirect(r'^firefox/brand/identity/wordmarks/$', 'styleguide.identity.firefox-wordmarks'),
    redirect(r'^firefox/brand/identity/typefaces/$', 'styleguide.communications.typefaces'),
    redirect(r'^firefox/brand/artwork/$', 'styleguide.home'),
    redirect(r'^firefox/brand/artwork/gear/$', 'styleguide.home'),
    redirect(r'^firefox/brand/website/$', 'styleguide.websites.sandstone-intro'),
    redirect(r'^firefox/brand/website/domain-strategy/$', 'styleguide.websites.domains-overview'),
    redirect(r'^firefox/brand/copy/$', 'styleguide.communications.copy-tone'),
    redirect(r'^firefox/brand/copy/l10n/$', 'styleguide.communications.translation'),
    redirect(r'^firefox/brand/copy/rules/$', 'styleguide.communications.copy-rules'),
    redirect(r'^firefox/brand/downloads/$', 'styleguide.home'),

    # Bug 804810 Identity Guidelines -> Style Guide
    redirect(r'^foundation/identity-guidelines/index.html', 'styleguide.home'),
    redirect(r'^foundation/identity-guidelines/mozilla-foundation.html', 'styleguide.identity.mozilla-branding'),
    redirect(r'^foundation/identity-guidelines/thunderbird.html', 'styleguide.identity.thunderbird-logo'),

    # Bug 800467 /apps/partners -> marketplace.m.o/developers
    redirect(r'apps/partners/$', 'https://marketplace.mozilla.org/developers/'),

    # Bug 815527 /m/privacy.html -> /legal/privacy/firefox.html
    redirect(r'^m/privacy.html$', '/legal/privacy/firefox.html'),

    # Bug 821047 /about/mission.html -> /mission/
    redirect(r'^about/mission.html$', '/mission/'),

    # Bug 800298 /webmaker/ -> wm.o and /webmaker/videos/ -> wm.o/videos/
    redirect(r'webmaker/$', 'https://webmaker.org'),
    redirect(r'webmaker/videos/$', 'https://webmaker.org/videos/'),

    # Bug 819317 /gameon/ -> gameon.m.o
    redirect(r'gameon/$', 'https://gameon.mozilla.org'),

    # Tabzilla
    redirect(r'tabzilla/media/js/tabzilla\.js$', '/tabzilla/tabzilla.js'),
    redirect(r'tabzilla/media/css/tabzilla\.css$',
             lambda r: '/media/css/tabzilla.less.css' if settings.TEMPLATE_DEBUG
                       else '/media/css/tabzilla-min.css'),
)
