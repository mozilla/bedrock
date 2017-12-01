from django.db import models


class ExternalFile(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    content = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'externalfiles'
