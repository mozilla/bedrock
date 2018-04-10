from django.conf import settings
from django.db import models

from django_extensions.db.fields.json import JSONField

from lib.l10n_utils.utils import parse, parse_tags


class LangFileManager(models.Manager):
    def refresh(self):
        """Reload data from the filesystem"""
        self.all().delete()
        count = 0
        for pathobj in settings.LOCALES_PATH.rglob('*.lang'):
            pathstr = str(pathobj)
            relpath = pathobj.relative_to(settings.LOCALES_PATH)
            locale = relpath.parts[0]
            name = str(relpath.relative_to(locale).with_suffix(''))
            translations = parse(pathstr)
            tags = parse_tags(pathstr)
            self.create(name=name,
                        locale=locale,
                        translations=translations,
                        tags=tags)
            count += 1

        return count

    def get_active_locales(self, name):
        """Return a list of locales available and active for a langfile name"""
        filters = {'name': name}
        if not settings.DEV:
            filters['tags__contains'] = '"active"'
        return [l.locale for l in self.filter(**filters)]

    def get_translations(self, name, locale):
        try:
            return self.get(name=name, locale=locale).translations
        except models.ObjectDoesNotExist:
            return {}

    def get_tags(self, name, locale):
        try:
            return self.get(name=name, locale=locale).tags
        except models.ObjectDoesNotExist:
            return []


class LangFile(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    locale = models.CharField(max_length=8, db_index=True)
    translations = JSONField(default={})
    tags = JSONField(default=[])

    objects = LangFileManager()

    class Meta:
        unique_together = (('name', 'locale'),)

    def __unicode__(self):
        return '%s/%s.lang' % (self.locale, self.name)

    def has_tag(self, tagname):
        return tagname in self.tags

    def is_active(self):
        return self.has_tag('active')
