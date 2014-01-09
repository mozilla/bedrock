# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin

from . import models


class NoteAdmin(admin.ModelAdmin):
    list_display = ('bug', 'tag', 'html')
    list_display_links = ('html',)
    filter_horizontal = ('releases',)


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('version', 'product', 'channel', 'is_public',
                    'release_date', 'text')


admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Release, ReleaseAdmin)
