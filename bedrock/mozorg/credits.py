# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv
import unicodedata
from collections import OrderedDict
from operator import itemgetter


from bedrock.externalfiles import ExternalFile


class CreditsFile(ExternalFile):
    def validate_content(self, content):
        rows = list(csv.reader(content.strip().split('\n')))
        if len(rows) < 2200:  # it's 2273 as of now
            raise ValueError('Much smaller file than expected. {0} rows.'.format(len(rows)))

        if len(rows[0]) != 2 or len(rows[-1]) != 2:
            raise ValueError('CSV Content corrupted.')

        return content

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
        for row in csv.reader(self.readlines()):
            if len(row) == 1:
                name = sortkey = row[0]
            elif len(row) == 2:
                name, sortkey = row
            else:
                continue

            sortkey = unicodedata.normalize('NFKD', sortkey).encode('ascii', 'ignore').decode()
            names.append([name, sortkey.upper()])

        return sorted(names, key=itemgetter(1))
