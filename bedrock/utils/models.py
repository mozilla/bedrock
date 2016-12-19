from django.db import models


class GitRepoState(models.Model):
    repo_id = models.CharField(max_length=100, db_index=True, unique=True)
    latest_ref = models.CharField(max_length=100)
