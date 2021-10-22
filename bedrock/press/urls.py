# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from . import views

urlpatterns = (
    url("^speakerrequest/$", views.SpeakerRequestView.as_view(), name="press.speaker-request"),
    url("^press-inquiry/$", views.PressInquiryView.as_view(), name="press.press-inquiry"),
)
