from django.conf.urls.defaults import *
from redirects.util import redirect_external

urlpatterns = patterns('',
    redirect_external('videos', 'https://webmaker.org/videos/'),
    redirect_external('', 'https://webmaker.org'),
)
