from bedrock.redirects.util import redirect


redirectpatterns = (
    redirect(r'^b2g', 'firefox.partners.index'),

    # Bug 781914
    redirect(r'^contribute/areas.html$', 'mozorg.contribute'),
    redirect(r'^contribute/universityambassadors',
             'mozorg.contribute.studentambassadors.landing'),

    # Bug 1144949
    redirect(r'^contribute/page/?$',
             'https://wiki.mozilla.org/Webdev/GetInvolved/mozilla.org'),

    # Bug 763665, 1148127
    redirect(r'^projects/$', 'firefox.family.index'),


    # Bug 792185 Brand Toolkit -> Style Guide
    redirect(r'^firefox/brand/$', 'styleguide.home'),
    redirect(r'^firefox/brand/platform/$',
             'styleguide.identity.firefox-family-platform'),
    redirect(r'^firefox/brand/identity/$',
             'styleguide.identity.firefox-branding'),
    redirect(r'^firefox/brand/identity/channel-logos/$',
             'styleguide.identity.firefox-channels'),
    redirect(r'^firefox/brand/identity/wordmarks/$',
             'styleguide.identity.firefox-wordmarks'),
    redirect(r'^firefox/brand/identity/typefaces/$',
             'styleguide.communications.typefaces'),
    redirect(r'^firefox/brand/artwork/$', 'styleguide.home'),
    redirect(r'^firefox/brand/artwork/gear/$', 'styleguide.home'),
    redirect(r'^firefox/brand/website/$',
             'styleguide.websites.sandstone-intro'),
    redirect(r'^firefox/brand/website/domain-strategy/$',
             'styleguide.websites.domains-overview'),
    redirect(r'^firefox/brand/copy/$', 'styleguide.communications.copy-tone'),
    redirect(r'^firefox/brand/copy/l10n/$',
             'styleguide.communications.translation'),
    redirect(r'^firefox/brand/copy/rules/$',
             'styleguide.communications.copy-rules'),
    redirect(r'^firefox/brand/downloads/$', 'styleguide.home'),

    # Bug 1186373
    redirect(r'^firefox/hello/npssurvey/$',
             'https://www.surveygizmo.com/s3/2227372/Firefox-Hello-Product-Survey',
             permanent=False),

    # Bug 1071318
    redirect(r'^firefox/mobile/$', 'firefox.android.index'),

    # Bug 804810 Identity Guidelines -> Style Guide
    redirect(r'^foundation/identity-guidelines/index.html', 'styleguide.home'),
    redirect(r'^foundation/identity-guidelines/mozilla-foundation.html',
             'styleguide.identity.mozilla-branding'),
    redirect(r'^foundation/identity-guidelines/thunderbird.html',
             'styleguide.identity.thunderbird-logo'),

    # Bug 945474 - delete Marketplace marketing product page
    # and redirect
    redirect(r'^apps/$', 'https://marketplace.firefox.com/'),

    # Bug 800467 /apps/partners ->
    # marketplace.firefox.com/developers
    redirect(r'apps/partners/$',
             'https://marketplace.firefox.com/developers/'),

    # Bug 815527 /m/privacy.html -> /privacy/firefox/
    redirect(r'^m/privacy.html$', 'privacy.notices.firefox'),

    # Bug 1109318 /privacy/you -> privacy/tips/
    redirect(r'^privacy/you/$',
             'privacy.privacy-day'),

    # Bug 821047 /about/mission.html -> /mission/
    redirect(r'^about/mission.html$', '/mission/'),

    # Bug 1171763 - delete researchers and projects and redirect
    redirect(r'^research/.+', '/research/'),

    # Bug 800298 /webmaker/ -> wm.o and /webmaker/videos/ ->
    # wm.o/videos/
    redirect(r'webmaker/$', 'https://webmaker.org'),
    redirect(r'webmaker/videos/$', 'https://webmaker.org/videos/'),

    # Bug 819317 /gameon/ -> gameon.m.o
    redirect(r'gameon/$', 'https://gameon.mozilla.org'),

    # Bug 822817 /telemetry/ ->
    # https://wiki.mozilla.org/Telemetry/FAQ
    redirect(r'telemetry/$', 'https://wiki.mozilla.org/Telemetry/FAQ'),

    # Bug 854561 - move /projects/mozilla-based/ to
    # /about/mozilla-based/
    redirect(r'^projects/mozilla-based/$', '/about/mozilla-based/'),

    # Bug 867773 - Redirect the Persona "Developer FAQ" link
    # to MDN
    redirect(r'^persona/developer-faq/$',
             'https://developer.mozilla.org/persona'),

    # Bug 981176 - For now we'll hard-code a redirect to 1.3
    # In the future this should automatically go to the
    # latest version's notes
    redirect(r'^firefox/os/notes/$', '/firefox/os/notes/1.3/'),

    # Bug 896585 - Send /contact/ to the spaces landing
    redirect(r'^contact/$', '/contact/spaces/'),

    # Bug 997577 - /legal/ -> /about/legal/
    redirect(r'^legal/fraud-report/$', '/about/legal/fraud-report/'),
    redirect(r'^legal/eula/$', '/about/legal/eula/'),
    redirect(r'^legal/eula/firefox-2/$', '/about/legal/eula/firefox-2/'),
    redirect(r'^legal/eula/firefox-3/$', '/about/legal/eula/firefox-3/'),

    # Bug 1073269 /dnt/ -> /firefox/dnt/
    redirect(r'^dnt/$', 'firefox.dnt'),
)
