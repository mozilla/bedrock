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

    # Bug 800467 /apps/partners -> marketplace.m.o/developers
    redirect(r'apps/partners/$', 'https://marketplace.mozilla.org/developers/'),
)
