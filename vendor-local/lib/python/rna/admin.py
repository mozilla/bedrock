# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin

from . import models


admin.site.register(models.Channel)
admin.site.register(models.Product)
admin.site.register(models.Tag)
admin.site.register(models.Note)
