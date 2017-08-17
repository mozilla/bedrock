#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import datetime
import os
import sys
from subprocess import check_call

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from decouple import config
from pathlib2 import Path


schedule = BlockingScheduler()
DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', default='')

# ROOT path of the project. A pathlib.Path object.
ROOT_PATH = Path(__file__).resolve().parents[1]
ROOT = str(ROOT_PATH)
MANAGE = str(ROOT_PATH / 'manage.py')


def call_command(command):
    check_call('python {0} {1}'.format(MANAGE, command), shell=True)


class scheduled_job(object):
    """Decorator for scheduled jobs. Takes same args as apscheduler.schedule_job."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fn):
        self.name = fn.__name__
        self.callback = fn
        schedule.add_job(self.run, id=self.name, *self.args, **self.kwargs)
        self.log('Registered')
        return self.run

    def run(self):
        self.log('starting')
        try:
            self.callback()
        except Exception as e:
            self.log('CRASHED: {}'.format(e))
            raise
        else:
            self.log('finished successfully')

    def log(self, message):
        msg = '[{}] Clock job {}@{}: {}'.format(
            datetime.datetime.utcnow(), self.name,
            os.getenv('DEIS_APP', 'default_app'), message)
        print(msg, file=sys.stderr)


def ping_dms(function):
    """Pings Dead Man's Snitch after job completion if URL is set."""

    def _ping():
        function()
        if DEAD_MANS_SNITCH_URL:
            utcnow = datetime.datetime.utcnow()
            payload = {'m': 'Run {} on {}'.format(function.__name__, utcnow.isoformat())}
            requests.get(DEAD_MANS_SNITCH_URL, params=payload)

    _ping.__name__ = function.__name__
    return _ping


def schedule_database_jobs():
    @scheduled_job('interval', minutes=15)
    @ping_dms
    def update_product_details():
        call_command('update_product_details_files --database bedrock')

    @scheduled_job('interval', minutes=30)
    def update_externalfiles():
        call_command('update_externalfiles')

    @scheduled_job('interval', minutes=30)
    def update_security_advisories():
        call_command('update_security_advisories')

    @scheduled_job('interval', hours=6)
    def update_tweets():
        call_command('cron update_tweets')

    @scheduled_job('interval', hours=1)
    def ical_feeds():
        call_command('cron update_ical_feeds')
        call_command('cron cleanup_ical_events')

    @scheduled_job('interval', hours=1)
    def update_blog_feeds():
        call_command('update_wordpress --database bedrock')


def schedul_l10n_jobs():
    @scheduled_job('interval', minutes=10)
    def update_locales():
        call_command('l10n_update')

    @scheduled_job('interval', minutes=5)
    def update_release_notes():
        call_command('update_release_notes --quiet')


if __name__ == '__main__':
    args = sys.argv[1:]
    has_jobs = False
    if 'db' in args:
        schedule_database_jobs()
        has_jobs = True
    if 'l10n' in args:
        schedul_l10n_jobs()
        has_jobs = True

    if has_jobs:
        try:
            schedule.start()
        except (KeyboardInterrupt, SystemExit):
            pass
