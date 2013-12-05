# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from rest_framework.filters import DjangoFilterBackend
import django_filters

from . import fields, models


class ISO8601DateTimeFilter(django_filters.DateTimeFilter):
    field_class = fields.ISO8601DateTimeField


class TimestampedFilterBackend(DjangoFilterBackend):
    def get_filter_class(self, view, queryset=None):
        filter_class = getattr(view, 'filter_class', None)
        filter_fields = getattr(view, 'filter_fields', None)
        filter_fields_exclude = getattr(view, 'filter_fields_exclude', ())

        if filter_class or filter_fields:
            return super(TimestampedFilterBackend, self).get_filter_class(
                view, queryset=queryset)

        elif queryset and issubclass(queryset.model, models.TimeStampedModel):
            class AutoFilterSet(self.default_filter_set):
                created_before = ISO8601DateTimeFilter(
                    name='created', lookup_type='lt')
                created_after = ISO8601DateTimeFilter(
                    name='created', lookup_type='gte')

                modified_before = ISO8601DateTimeFilter(
                    name='modified', lookup_type='lt')
                modified_after = ISO8601DateTimeFilter(
                    name='modified', lookup_type='gte')

                class Meta:
                    model = queryset.model
                    fields = ['created_before', 'created_after',
                              'modified_before', 'modified_after']
                    fields.extend(f.name for f in model._meta.fields
                                  if f.name not in ('created', 'modified'))
                    fields = [f for f in fields
                              if f not in filter_fields_exclude]
                    order_by = True
            return AutoFilterSet
