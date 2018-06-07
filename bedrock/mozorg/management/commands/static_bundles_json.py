from __future__ import print_function, unicode_literals

import json

from django.core.management.base import BaseCommand

from bedrock.settings.static_media import PIPELINE_CSS, PIPELINE_JS


class Command(BaseCommand):
    """Command to output pipeline bundle configs as JSON.

    TODO: Delete me after pipeline removal.
    """
    def handle(self, *args, **options):
        output = {
            'css': [],
            'js': [],
        }
        for name, bundle in PIPELINE_CSS.iteritems():
            output['css'].append({
                'name': name,
                'files': bundle['source_filenames'],
            })
        for name, bundle in PIPELINE_JS.iteritems():
            output['js'].append({
                'name': name,
                'files': bundle['source_filenames'],
            })

        print(json.dumps(output, indent=2))
