# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('channels', views.ChannelViewSet)
router.register('notes', views.NoteViewSet)
router.register('products', views.ProductViewSet)
router.register('releases', views.ReleaseViewSet)
router.register('tags', views.TagViewSet)

urlpatterns = router.urls
