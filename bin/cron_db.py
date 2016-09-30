#!/usr/bin/env python

from __future__ import print_function, unicode_literals

from apscheduler.schedulers.blocking import BlockingScheduler

from scheduler_utils import call_command, scheduled_job, ping_dms


schedule = BlockingScheduler()


@scheduled_job(schedule, 'interval', minutes=30)
@ping_dms
def update_product_details():
    call_command('update_product_details_files --database bedrock')


@scheduled_job(schedule, 'interval', minutes=30)
def update_externalfiles():
    call_command('update_externalfiles')


@scheduled_job(schedule, 'interval', minutes=30)
def update_security_advisories():
    call_command('update_security_advisories')


@scheduled_job(schedule, 'interval', minutes=5)
def rnasync():
    # running in a subprocess as rnasync was not designed for long-running process
    call_command('rnasync')


@scheduled_job(schedule, 'interval', hours=6)
def update_tweets():
    call_command('cron update_tweets')


@scheduled_job(schedule, 'interval', hours=1)
def ical_feeds():
    call_command('cron update_ical_feeds')
    call_command('cron cleanup_ical_events')


@scheduled_job(schedule, 'interval', hours=1)
def update_firefox_os_feeds():
    call_command('runscript update_firefox_os_feeds')


if __name__ == '__main__':
    try:
        schedule.start()
    except (KeyboardInterrupt, SystemExit):
        pass
