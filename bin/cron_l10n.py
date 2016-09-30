#!/usr/bin/env python

from __future__ import print_function, unicode_literals

from apscheduler.schedulers.blocking import BlockingScheduler

from bedrock.scheduler_utils import call_command, scheduled_job


schedule = BlockingScheduler()


@scheduled_job(schedule, 'interval', minutes=10)
def update_locales():
    call_command('l10n_update')


if __name__ == '__main__':
    try:
        schedule.start()
    except (KeyboardInterrupt, SystemExit):
        pass
