#!/usr/bin/env python


import os
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


if __name__ == '__main__':
    calendars_dir = os.path.join('media','caldata')
    ics_files = map(lambda x: os.path.join(calendars_dir, x), 
                    filter(get_ics, os.listdir(calendars_dir)))
    
    format_str = "Failed to parse the icalendar file: {}. {}"
    check_failed = False
    for f in ics_files:
        try:
            check_if_correct_parse(f)
        except ValueError as ve:
            check_failed = True
            print format_str.format(f, ve.message)

    if check_failed:
        # Returning a positive error code, since we have nothing to do
        # with these errors. They simply have to be reported back to
        # caldata maintainers. Also, we have to return something
        # other than zero - for travis to fail build over invalid files. 
        # Please see: http://docs.travis-ci.com/user/build-lifecycle/
        # """
        #   When any of the steps in the script stage fails with a non-zero 
        #   exit code, the build will be marked as failed.
        # """
        exit(1)


# vim: ts=4 sw=4 et ai
