from django.conf.urls.defaults import *
from util import redirect

urlpatterns = patterns('',

    redirect(r'^b2g', 'firefoxos.firefoxos'),
    redirect(r'^b2g/faq', 'firefoxos.firefoxos'),
    redirect(r'^b2g/about', 'firefoxos.firefoxos'),

    redirect(r'^contribute/areas.html$', 'mozorg.contribute'),  # Bug 781914
    redirect(r'^projects/$', 'mozorg.products'),  # Bug 763665

    )
