from django.db import models
from django.utils.safestring import mark_safe
from data import GRANT_LIST, FOCUS_OPTIONS, CURRENCY_OPTIONS
from operator import attrgetter
import warnings
import hashlib


class GrantQuerySet (object):
    def __init__ (self, model=None, **kwargs):
        self.model = model
        self._result_cache = [self.model(**item) for item in GRANT_LIST]
        self.order_by(*self.model._meta.ordering)

    def __iter__ (self):
        return iter(self._result_cache)

    def __call__ (self, *args, **kwargs):
        print (args, kwargs)

    def __getattr__ (self, name):
        warnings.warn("This method is not supported by %s" % self.__class__.__name__, RuntimeWarning)
        return self

    def __getitem__(self, k):
        if not isinstance(k, (slice, int, long)):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0))
                or (isinstance(k, slice) and (k.start is None or k.start >= 0)
                    and (k.stop is None or k.stop >= 0))), \
                "Negative indexing is not supported."

        return self._result_cache[k]

    def count (self):
        return len(self._result_cache)

    def order_by (self, *field_names):
        for name in reversed(field_names):
            if name[0] == '-':
                name = name[1:]
                reverse = True
            else:
                reverse = False

            self._result_cache.sort(key=attrgetter(name), reverse=reverse)

        return self

    def _filter (self, query):
        def f (grant):
            for key, value in query.items():
                try:
                    attr, comparator = key.split('__', 2)
                except ValueError:
                    attr = key
                    comparator = 'eq'

                comparator = comparator.lower()

                val = getattr(grant, attr, None)

                if comparator == 'lte':
                    if val > value:
                        return False
                elif comparator == 'lt':
                    if val >= value:
                        return False
                elif comparator == 'gte':
                    if val < value:
                        return False
                elif comparator == 'gt':
                    if val <= value:
                        return False
                elif comparator == 'ne':
                    if val == value:
                        return False
                elif comparator == 'eq':
                    if val != value:
                        return False
                else:
                    raise Exception()
            return True

        return f

    def filter (self, **query):
        # A very naive filtering function
        self._result_cache = filter(self._filter(query), self._result_cache)
        return self

    def get (self, **query):
        self.filter(**query)
        result_count = len(self._result_cache)

        if result_count == 1:
            return self._result_cache[0]
        elif result_count > 1:
            raise self.model.MultipleObjectsReturned()
        else:
            raise self.model.DoesNotExist()


class GrantManager (models.Manager):
    def get_query_set (self):
        return GrantQuerySet(self.model, using=self._db)


class Grant (models.Model):
    grantee = models.CharField(max_length=200)
    title = models.CharField(max_length=200, verbose_name='Project Title', primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_OPTIONS, default='USD')
    year = models.IntegerField()
    focus = models.CharField(max_length=20, choices=FOCUS_OPTIONS)
    summary = models.CharField(max_length=300)
    slug = models.SlugField(max_length=100)

    class Meta:
        managed = False
        ordering = ['year', '-title']

    grants = GrantManager()

    def __unicode__ (self):
        return '%s: %s' % (self.grantee, self.title)

    @models.permalink
    def get_absolute_url (self):
        return ('grants.single', (), {'slug': self.slug});

    @property
    def focus_area (self):
        return self.get_focus_display()

    @property
    def value (self):
        return '%s %s' % (self.currency, self.amount)

    @property
    def formatted_value (self):
        return mark_safe(self.get_currency_display() % self.amount)
