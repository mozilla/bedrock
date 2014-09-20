# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.functional import total_ordering

from django_extensions.db.fields import ModificationDateTimeField
from django_extensions.db.fields.json import JSONField
from funfactory.urlresolvers import reverse
from product_details.version_compare import Version


@total_ordering
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, db_index=True)
    product = models.CharField(max_length=50)
    product_slug = models.SlugField()

    class Meta:
        ordering = ('slug',)

    def __unicode__(self):
        return self.name

    @property
    def name_tuple(self):
        name, vers = self.name.rsplit(None, 1)
        if '.' not in vers:
            vers += '.0'
        return name, Version(vers)

    @property
    def version(self):
        return self.name_tuple[1]

    def __lt__(self, other):
        return self.name_tuple < other.name_tuple

    def get_absolute_url(self):
        return reverse('security.product-version-advisories',
                       kwargs={'slug': self.slug})

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        self.product = self.name_tuple[0]
        self.product_slug = slugify(self.product)
        self.slug = '{0}-{1}'.format(self.product_slug, self.version)
        super(Product, self).save(force_insert, force_update,
                                  using, update_fields)


class SecurityAdvisory(models.Model):
    id = models.CharField(max_length=8, primary_key=True, db_index=True)
    title = models.CharField(max_length=200)
    impact = models.CharField(max_length=100)
    reporter = models.CharField(max_length=100, null=True)
    announced = models.DateField(null=True)
    year = models.SmallIntegerField()
    order = models.SmallIntegerField()
    fixed_in = models.ManyToManyField(Product, related_name='advisories')
    extra_data = JSONField()
    html = models.TextField()
    last_modified = ModificationDateTimeField()

    class Meta:
        ordering = ('-year', '-order')
        get_latest_by = 'last_modified'

    def __unicode__(self):
        return u'MFSA {0}'.format(self.id)

    def get_absolute_url(self):
        return reverse('security.advisory', kwargs={'pk': self.id})

    @property
    def impact_class(self):
        return self.impact.lower().split(None, 1)[0]

    @property
    def products(self):
        prods_set = set(v.product for v in self.fixed_in.all())
        return sorted(prods_set)
