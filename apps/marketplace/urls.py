from django.conf.urls.defaults import *
from views import marketplace
from bedrock_util import secure_required

urlpatterns = patterns('',
    (r'^$', secure_required(marketplace)),
)
