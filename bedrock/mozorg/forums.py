# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.utils.functional import cached_property

from ordereddict import OrderedDict

from bedrock.svnfiles import SVNFile


class ForumsFile(SVNFile):
    forum_line_re = re.compile(r'^((?:mozilla\.)?[a-z0-9\-\.]+)\s+(.*)$')
    title_line_re = re.compile(r'^:(.*)$')

    def __init__(self):
        super(ForumsFile, self).__init__('forums')

    @cached_property
    def ordered(self):
        forums = OrderedDict()
        current_group = None
        for line in self.readlines():
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


forums_file = ForumsFile()
