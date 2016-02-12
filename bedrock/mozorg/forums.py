# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
import codecs
from collections import OrderedDict

from django.conf import settings


class ForumsFile(object):
    source_path = os.path.join(settings.MEDIA_ROOT, 'forums', 'raw-ng-list.txt')
    forum_line_re = re.compile(r'^((?:mozilla\.)?[a-z0-9\-\.]+)\s+(.*)$')
    title_line_re = re.compile(r'^:(.*)$')

    def validate_content(self, content):
        lines = content.split('\n')
        try:
            forums = self._parse(lines)
        except Exception:
            raise ValueError('Error parsing forums file.')

        # currently 15 categories
        if not len(forums.keys()) > 10:
            raise ValueError('Forums file truncated or corrupted.')

        return lines

    def read(self):
        try:
            content = codecs.open(self.source_path, 'r', 'utf-8').read()
        except Exception:
            raise ValueError('Error opening forums file.')

        return content

    def readlines(self):
        return self.validate_content(self.read())

    @property
    def ordered(self):
        return self._parse(self.readlines())

    def _parse(self, lines):
        forums = OrderedDict()
        current_group = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            title_m = self.title_line_re.match(line)
            if title_m:
                current_group = forums[title_m.group(1)] = []

            elif current_group is not None:
                forum_m = self.forum_line_re.match(line)
                if forum_m:
                    forum_id, forum_desc = forum_m.groups()
                    forum_id_dashed = re.sub(r'^mozilla\.', '', forum_id)
                    forum_id_dashed = forum_id_dashed.replace('.', '-')
                    current_group.append({
                        'id': forum_id,
                        'dashed': forum_id_dashed,
                        'description': forum_desc,
                    })

        return forums
