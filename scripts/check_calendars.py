#!/usr/bin/env python

from __future__ import print_function
import os
import sys

from icalendar import Calendar


def get_ics(filename):
    return filename.endswith('ics')


def check_if_correct_parse(ics_file):
    fh = open(ics_file, 'rb')
    try:
        # some calendars, such as Austrian ones have multiple
        # vCalendar entries - we probably don't want them to fail
        # parse. So we set multiple=True below
        cal_entries = Calendar.from_ical(fh.read(), multiple=True)
        if cal_entries is None:
            raise ValueError
    finally:
        fh.close()


def run(*args):
    calendars_dir = os.path.join('media', 'caldata')
    ics_files = map(lambda x: os.path.join(calendars_dir, x),
                    filter(get_ics, os.listdir(calendars_dir)))

    format_str = "Failed to parse the icalendar file: {}. {}"
    check_failed = False
    for f in ics_files:
        try:
            check_if_correct_parse(f)
        except ValueError as ve:
            check_failed = True
            print(format_str.format(f, ve.message))

    if check_failed:
        sys.exit(1)


# vim: ts=4 sw=4 et ai
