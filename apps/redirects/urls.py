from django.conf.urls.defaults import *
from util import redirect

urlpatterns = patterns('',

    redirect(r'^b2g', 'firefoxos.firefoxos'),
    redirect(r'^b2g/faq', 'firefoxos.firefoxos'),
    redirect(r'^b2g/about', 'firefoxos.firefoxos'),

    )
