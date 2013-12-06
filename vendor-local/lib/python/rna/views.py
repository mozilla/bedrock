# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from rest_framework.viewsets import ModelViewSet

from . import models


class ChannelViewSet(ModelViewSet):
    model = models.Channel


class ProductViewSet(ModelViewSet):
    model = models.Product


class TagViewSet(ModelViewSet):
    model = models.Tag


class NoteViewSet(ModelViewSet):
    model = models.Note


class ReleaseViewSet(ModelViewSet):
    model = models.Release
