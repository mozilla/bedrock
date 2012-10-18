from django.conf.urls.defaults import *

from mozorg.util import page

urlpatterns = patterns('',
    # /apps is temporarily redirected to /apps/partners as per
    # https://bugzilla.mozilla.org/show_bug.cgi?id=751903
    page('', 'marketplace/marketplace.html'),
)
