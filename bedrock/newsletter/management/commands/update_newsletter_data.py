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

        count = Newsletter.objects.refresh(newsletters)
        if not options['quiet']:
            if count:
                print('Updated %d newsletters' % count)
            else:
                print('Nothing to update')
