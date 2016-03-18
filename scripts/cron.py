from __future__ import print_function
import datetime
import os
import sys
from subprocess import check_call

from django.core.management import call_command
from django.conf import settings

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from bedrock.events.cron import cleanup_ical_events, update_ical_feeds
from bedrock.mozorg.cron import update_tweets
from scripts import update_firefox_os_feeds


schedule = BlockingScheduler()


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
        if settings.DEAD_MANS_SNITCH_URL:
            utcnow = datetime.datetime.utcnow()
            payload = {'m': 'Run {} on {}'.format(function.__name__, utcnow.isoformat())}
            requests.get(settings.DEAD_MANS_SNITCH_URL, params=payload)

    _ping.__name__ = function.__name__
    return _ping


@scheduled_job('interval', minutes=30)
@ping_dms
def job_update_product_details():
    call_command('update_product_details')


@scheduled_job('interval', minutes=30)
def job_update_externalfiles():
    call_command('update_externalfiles')


@scheduled_job('interval', minutes=30)
def job_update_security_advisories():
    call_command('update_security_advisories')


@scheduled_job('interval', minutes=5)
def job_rnasync():
    # running in a subprocess as rnasync was not designed for long-running process
    check_call('python {} rnasync'.format(os.path.join(settings.ROOT, 'manage.py')),
               shell=True)


@scheduled_job('interval', hours=6)
def job_update_tweets():
    update_tweets()


@scheduled_job('interval', hours=1)
def job_ical_feeds():
    update_ical_feeds()
    cleanup_ical_events()


@scheduled_job('interval', hours=1)
def job_update_firefox_os_feeds():
    update_firefox_os_feeds.run()


def run():
    try:
        schedule.start()
    except (KeyboardInterrupt, SystemExit):
        pass
