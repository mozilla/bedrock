from django.conf.urls.defaults import *
from views import marketplace, partners
from bedrock_util import secure_required

urlpatterns = patterns('',
    (r'^$', secure_required(marketplace)),
    (r'^partners/$', secure_required(partners)),
)
