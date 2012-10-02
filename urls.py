from django.conf import settings
from django.conf.urls.defaults import *

from funfactory.monkeypatches import patch
patch()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# The default django 500 handler doesn't run the ContextProcessors, which breaks
# the base template page. So we replace it with one that does!
handler500 = 'bedrock_util.server_error_view'

urlpatterns = patterns('',
    # Main pages
    (r'^b2g/', include('b2g.urls')),
    (r'^webmaker/', include('webmaker.urls')),
    (r'^gameon/', include('gameon.urls')),
    (r'^grants/', include('grants.urls')),
    (r'^collusion/', include('collusion.urls')),
    (r'^apps/', include('marketplace.urls')),
    (r'^persona/', include('persona.urls')),
    (r'^styleguide/', include('styleguide.urls')),
    (r'', include('firefox.urls')),
    (r'', include('mozorg.urls')),
    (r'^privacy/', include('privacy.urls')),
    (r'', include('research.urls')),

    # L10n example.
    (r'^l10n_example/', include('l10n_example.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

