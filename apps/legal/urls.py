from django.conf.urls.defaults import *
from mozorg.util import page

urlpatterns = patterns('',
    page('eula', 'eula/index.html'),
)