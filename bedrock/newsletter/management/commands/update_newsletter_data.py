from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

import basket

from bedrock.newsletter.models import Newsletter


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        newsletters = basket.get_newsletters()
        if not newsletters:
            raise CommandError('No data from basket')

        Newsletter.objects.all().delete()
        count = 0
        for slug, data in newsletters.iteritems():
            Newsletter.objects.create(
                slug=slug,
                data=data,
            )
            count += 1

        if not options['quiet']:
            print('Updated %d newsletters' % count)
