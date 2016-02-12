# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import csv
import codecs
from collections import OrderedDict
from operator import itemgetter

from django.conf import settings


class CreditsFile(object):
    source_path = os.path.join(settings.MEDIA_ROOT, 'credits', 'names.csv')

    def validate_content(self, content):
        rows = list(csv.reader(content.strip().encode('utf8').split('\n')))
        if len(rows) < 2200:  # it's 2273 as of now
            raise ValueError('Much smaller file than expected. {0} rows.'.format(len(rows)))

        if len(rows[0]) != 2 or len(rows[-1]) != 2:
            raise ValueError('CSV Content corrupted.')

        return rows

    def read(self):
        try:
            content = codecs.open(self.source_path, 'r', 'utf-8').read()
        except Exception:
            raise ValueError('Error opening credits file.')

        return content

    def readlines(self):
        return self.validate_content(self.read())

    @property
    def ordered(self):
        """
        Returns an OrderedDict of sorted lists of names by first letter of sortkey.

        :param credits_data: any iterable of CSV formatted strings.
        :return: OrderedDict
        """
        ordered_names = OrderedDict()
        for name, sortkey in self.rows:
            letter = sortkey[0]
            if letter not in ordered_names:
                ordered_names[letter] = []

            ordered_names[letter].append(name)

        return ordered_names

    @property
    def rows(self):
        """
        Returns a list of lists sorted by the sortkey column.

        :param credits_data: any iterable of CSV formatted strings.
        :return: list of lists
        """
        names = []
        for row in self.readlines():
            cols = row.split(',')
            if len(cols) == 1:
                name = sortkey = cols[0]
            elif len(cols) == 2:
                name, sortkey = cols
            else:
                continue

            names.append([name.decode('utf8'), sortkey.upper()])

        return sorted(names, key=itemgetter(1))
