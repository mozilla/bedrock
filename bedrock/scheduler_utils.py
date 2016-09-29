from __future__ import print_function, unicode_literals

import datetime
import os
import sys
from subprocess import check_call

import requests
from decouple import config
from pathlib import Path

DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', default='')
# ROOT path of the project. A pathlib.Path object.
ROOT_PATH = Path(__file__).resolve().parents[1]
ROOT = str(ROOT_PATH)
MANAGE = str(ROOT_PATH / 'manage.py')


def call_command(command):
    check_call('python {0} {1}'.format(MANAGE, command), shell=True)


class scheduled_job(object):
    """Decorator for scheduled jobs. Takes same args as apscheduler.schedule_job."""

    def __init__(self, schedule, *args, **kwargs):
        self.schedule = schedule
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fn):
        self.name = fn.__name__
        self.callback = fn
        self.schedule.add_job(self.run, id=self.name, *self.args, **self.kwargs)
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
