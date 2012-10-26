from django.conf.urls.defaults import *
from mozorg.util import page


urlpatterns = patterns('',

    page('foundation/annualreport/2011', 'foundation/annualreport/2011.html'),
    page('foundation/annualreport/2011/faq', 'foundation/annualreport/2011faq.html'),

)
