# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv
from operator import itemgetter

from django.utils.functional import cached_property

from ordereddict import OrderedDict

from bedrock.svnfiles import SVNFile


class CreditsFile(SVNFile):
    def __init__(self):
        super(CreditsFile, self).__init__('credits')

    @cached_property
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

            names.append([name.decode('utf8'), sortkey.upper()])

        return sorted(names, key=itemgetter(1))


credits_file = CreditsFile()
