from django.db import models

from picklefield import PickledObjectField
from django_extensions.db.fields import ModificationDateTimeField


CONTRIBUTOR_SOURCE_NAMES = {
    'all': None,
    'sumo': 'team',
    'reps': 'team',
    'qa': 'team',
    'firefox': 'team',
    'firefoxos': 'team',
    'firefoxforandroid': 'team',
    'bugzilla': 'source',
    'github': 'source',
}


class TwitterCache(models.Model):
    account = models.CharField(max_length=100, db_index=True, unique=True)
    tweets = PickledObjectField(default=list)
    updated = ModificationDateTimeField()


class ContributorActivityManager(models.Manager):
    def group_by_date_and_source(self, source):
        try:
            source_type = CONTRIBUTOR_SOURCE_NAMES[source]
        except KeyError:
            raise ContributorActivity.DoesNotExist

        qs = self.values('date')
        if source_type is not None:
            field_name = source_type + '_name'
            qs = qs.filter(**{field_name: source})

        # dates are grouped in weeks. 52 results gives us a year.
        return qs.annotate(models.Sum('total'), models.Sum('new'))[:52]


class ContributorActivity(models.Model):
    date = models.DateField()
    source_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    total = models.IntegerField()
    new = models.IntegerField()

    objects = ContributorActivityManager()

    class Meta:
        unique_together = ('date', 'source_name', 'team_name')
        get_latest_by = 'date'
        ordering = ['-date']
