from django.conf.urls.defaults import *
from mozorg.util import page


urlpatterns = patterns('',
    page('trans-block-reload-test', 'trans_block_reload_test.html'),
)
