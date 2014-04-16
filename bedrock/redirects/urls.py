# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import patterns

from util import redirect


def tabzilla_css_redirect(r):
    suffix = '/tabzilla.less' if settings.TEMPLATE_DEBUG else '-min'
    if settings.LESS_PREPROCESS:
        from jingo_minify.helpers import build_less
        build_less('css/tabzilla/tabzilla.less')

    return '%scss/tabzilla%s.css' % (settings.MEDIA_URL, suffix)


urlpatterns = patterns('',

    redirect(r'^b2g', 'firefox.partners.index'),
    redirect(r'^b2g/faq', 'firefox.partners.index'),
    redirect(r'^b2g/about', 'firefox.partners.index'),

    redirect(r'^contribute/areas.html$', 'mozorg.contribute'),  # Bug 781914
    redirect(r'^contribute/universityambassadors', 'mozorg.contribute.studentambassadors.landing'),
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

    # Bug 945474 - delete Marketplace marketing product page and redirect
    redirect(r'^apps/$', 'https://marketplace.firefox.com/'),

    # Bug 800467 /apps/partners -> marketplace.firefox.com/developers
    redirect(r'apps/partners/$', 'https://marketplace.firefox.com/developers/'),

    # Bug 815527 /m/privacy.html -> /privacy/firefox/
    redirect(r'^m/privacy.html$', 'privacy.notices.firefox'),

    # Bug 821047 /about/mission.html -> /mission/
    redirect(r'^about/mission.html$', '/mission/'),

    # Bug 800298 /webmaker/ -> wm.o and /webmaker/videos/ -> wm.o/videos/
    redirect(r'webmaker/$', 'https://webmaker.org'),
    redirect(r'webmaker/videos/$', 'https://webmaker.org/videos/'),

    # Bug 819317 /gameon/ -> gameon.m.o
    redirect(r'gameon/$', 'https://gameon.mozilla.org'),

    # Tabzilla
    redirect(r'tabzilla/media/js/tabzilla\.js$', 'tabzilla'),
    redirect(r'tabzilla/media/css/tabzilla\.css$', tabzilla_css_redirect),

    # Bug 822817 /telemetry/ -> https://wiki.mozilla.org/Telemetry/FAQ
    redirect(r'telemetry/$', 'https://wiki.mozilla.org/Telemetry/FAQ'),

    #Bug 854561 - move /projects/mozilla-based/ to /about/mozilla-based/
    redirect(r'^projects/mozilla-based/$', '/about/mozilla-based/'),

    # Bug 867773 - Redirect the Persona "Developer FAQ" link to MDN
    redirect(r'^persona/developer-faq/$', 'https://developer.mozilla.org/persona'),

    # Bug 981176 - For now we'll hard-code a redirect to 1.3
    # In the future this should automatically go to the latest version's notes
    redirect(r'^firefox/os/notes/$', '/firefox/os/notes/1.3/'),

    # Bug 896585 - Send /contact/ to the spaces landing
    redirect(r'^contact/$', '/contact/spaces/'),

    # Bug 944213 /foundation/annualreport/ -> /foundation/annualreport/20xx/
    redirect(r'^foundation/annualreport/$', 'foundation.annualreport.2012.index',
             name='foundation.annualreport'),
)
