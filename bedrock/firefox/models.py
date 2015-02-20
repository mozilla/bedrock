from django.db import models


class FirefoxOSFeedLink(models.Model):
    link = models.URLField(max_length=2000)
    title = models.CharField(max_length=2000)
    locale = models.CharField(max_length=10, db_index=True)

    def __unicode__(self):
        return self.title
