from django.conf.urls.defaults import *
from util import redirect

urlpatterns = patterns('',

    redirect(r'^b2g', 'firefoxos'),
    redirect(r'^b2g/faq', 'firefoxos'),
    redirect(r'^b2g/about', 'firefoxos'),
    
    )
