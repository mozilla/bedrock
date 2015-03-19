# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv
from operator import itemgetter

from ordereddict import OrderedDict

from bedrock.externalfiles import ExternalFile


class CreditsFile(ExternalFile):
    cache_key = 'credits-file-sorted-names'

    def validate_content(self, content):
        rows = list(csv.reader(content.strip().encode('utf8').split('\n')))
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
        sorted_names = self._cache.get(self.cache_key)
        if sorted_names is None:
            names = []
            for row in csv.reader(self.readlines()):
                if len(row) == 1:
                    name = sortkey = row[0]
                elif len(row) == 2:
                    name, sortkey = row
                else:
                    continue

                names.append([name.decode('utf8'), sortkey.upper()])

            sorted_names = sorted(names, key=itemgetter(1))
            self._cache.set(self.cache_key, 3600)  # 1 hour

        return sorted_names
