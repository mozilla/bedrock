# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from . import views

urlpatterns = (
    path("speakerrequest/", views.SpeakerRequestView.as_view(), name="press.speaker-request"),
    path("press-inquiry/", views.PressInquiryView.as_view(), name="press.press-inquiry"),
)
