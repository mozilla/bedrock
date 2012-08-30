from django.conf.urls.defaults import *
from mozorg.util import page

urlpatterns = patterns('',
    page('', 'styleguide/home.html'),
    page('identity/firefox/branding', 'styleguide/identity/firefox-branding.html'),
    page('identity/firefox/channels', 'styleguide/identity/firefox-channels.html'),
    page('identity/firefox/wordmarks', 'styleguide/identity/firefox-wordmarks.html'),
    page('identity/firefox/color', 'styleguide/identity/firefox-color.html'),

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
)
