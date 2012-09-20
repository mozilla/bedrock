from django.conf.urls.defaults import *
from mozorg.util import page

urlpatterns = patterns('',
    page('', 'styleguide/home.html'),

    page('identity/mozilla/branding', 'styleguide/identity/mozilla-branding.html'),
    page('identity/mozilla/color', 'styleguide/identity/mozilla-color.html'),
    page('identity/mozilla/innovations', 'styleguide/identity/mozilla-innovations.html'),

    page('identity/firefox/branding', 'styleguide/identity/firefox-branding.html'),
    page('identity/firefox/channels', 'styleguide/identity/firefox-channels.html'),
    page('identity/firefox/wordmarks', 'styleguide/identity/firefox-wordmarks.html'),
    page('identity/firefox/color', 'styleguide/identity/firefox-color.html'),

    page('identity/firefoxos/branding', 'styleguide/identity/firefoxos-branding.html'),

    page('identity/firefox-family/overview', 'styleguide/identity/firefox-family-overview.html'),
    page('identity/firefox-family/platform', 'styleguide/identity/firefox-family-platform.html'),

    page('identity/marketplace/branding', 'styleguide/identity/marketplace-branding.html'),
    page('identity/marketplace/color', 'styleguide/identity/marketplace-color.html'),

    page('identity/webmaker/branding', 'styleguide/identity/webmaker-branding.html'),
    page('identity/webmaker/color', 'styleguide/identity/webmaker-color.html'),

    page('identity/thunderbird/logo', 'styleguide/identity/thunderbird-logo.html'),
    page('identity/thunderbird/channels', 'styleguide/identity/thunderbird-channels.html'),
    page('identity/thunderbird/wordmarks', 'styleguide/identity/thunderbird-wordmarks.html'),
    page('identity/thunderbird/color', 'styleguide/identity/thunderbird-color.html'),

    page('websites/sandstone', 'styleguide/websites/sandstone-intro.html'),
    page('websites/sandstone/buttons', 'styleguide/websites/sandstone-buttons.html'),
    page('websites/sandstone/colors', 'styleguide/websites/sandstone-colors.html'),
    page('websites/sandstone/forms', 'styleguide/websites/sandstone-forms.html'),
    page('websites/sandstone/grids', 'styleguide/websites/sandstone-grids.html'),
    page('websites/sandstone/tables', 'styleguide/websites/sandstone-tables.html'),
    page('websites/sandstone/tabzilla', 'styleguide/websites/sandstone-tabzilla.html'),
    page('websites/sandstone/typefaces', 'styleguide/websites/sandstone-typefaces.html'),
    page('websites/sandstone/examples', 'styleguide/websites/sandstone-examples.html'),

    page('websites/community/overview', 'styleguide/websites/community-overview.html'),
    page('websites/domains/overview', 'styleguide/websites/domains-overview.html'),

    page('communications/presentations', 'styleguide/communications/presentations.html'),
    page('communications/video', 'styleguide/communications/video.html'),
    page('communications/typefaces', 'styleguide/communications/typefaces.html'),
    page('communications/copy-tone', 'styleguide/communications/copy-tone.html'),
    page('communications/copy-rules', 'styleguide/communications/copy-rules.html'),
    page('communications/translation', 'styleguide/communications/translation.html'),
)
