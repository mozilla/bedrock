#!/usr/bin/env python

import datetime
import platform
import sys
from subprocess import check_call
from time import time

import babis
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path

from db_s3_utils import DATA_PATH


# ROOT path of the project. A pathlib.Path object.
ROOT_PATH = Path(__file__).resolve().parents[1]
ROOT = str(ROOT_PATH)

# add bedrock to path
sys.path.append(ROOT)

# must import after adding bedrock to path
from bedrock.base.config_manager import config  # noqa

# these are the defaults, but explicit is better
JOB_DEFAULTS = {
    'coalesce': True,
    'max_instances': 1,
}
schedule = BlockingScheduler(job_defaults=JOB_DEFAULTS)

HOSTNAME = platform.node()
DB_UPDATE_MINUTES = config('DB_UPDATE_MINUTES', default='5', parser=int)
LOCAL_DB_UPDATE = config('LOCAL_DB_UPDATE', default='False', parser=bool)
DB_DOWNLOAD_IGNORE_GIT = config('DB_DOWNLOAD_IGNORE_GIT', default='False', parser=bool)
RUN_TIMES = {}

# Dead Man's Snitch
DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', default='')

MANAGE = str(ROOT_PATH / 'manage.py')
HEALTH_FILE_BASE = f'{DATA_PATH}/last-run'


def set_updated_time(name):
    check_call('touch {}-{}'.format(HEALTH_FILE_BASE, name), shell=True)


def call_command(command):
    check_call('python {0} {1}'.format(MANAGE, command), shell=True)


class scheduled_job:
    """Decorator for scheduled jobs. Takes same args as apscheduler.schedule_job."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fn):
        self.name = fn.__name__
        self.callback = fn
        schedule.add_job(self.run, id=self.name, *self.args, **self.kwargs)
        set_updated_time(self.name)
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
            set_updated_time(self.name)
            self.log('finished successfully')

    def log(self, message):
        msg = '[{}] Clock job {}@{}: {}'.format(
            datetime.datetime.utcnow(), self.name, HOSTNAME, message)
        print(msg, file=sys.stderr)


def set_last_run(name):
    RUN_TIMES[name] = time()


def get_time_since(name):
    last_run = RUN_TIMES.get(name)
    if last_run:
        return time() - last_run

    # initialize if not set
    set_last_run(name)
    return 0


def schedule_database_jobs():
    @scheduled_job('interval', minutes=DB_UPDATE_MINUTES)
    @babis.decorator(ping_after=DEAD_MANS_SNITCH_URL)
    def update_upload_database():
        fn_name = 'update_upload_database'
        command = 'bin/run-db-update.sh --auth'
        time_since = get_time_since(fn_name)
        if time_since > 21600:  # 6 hours
            command += ' --all'

        check_call(command, shell=True)
        if not LOCAL_DB_UPDATE:
            check_call('python bin/run-db-upload.py', shell=True)

        if command.endswith('--all'):
            # must set this after command run so that it won't update
            # if an update errors
            set_last_run(fn_name)


def schedule_file_jobs():
    @scheduled_job('interval', minutes=DB_UPDATE_MINUTES)
    def update_locales():
        call_command('l10n_update')

    if not LOCAL_DB_UPDATE:
        @scheduled_job('interval', minutes=DB_UPDATE_MINUTES)
        def download_database():
            command = 'python bin/run-db-download.py'
            if DB_DOWNLOAD_IGNORE_GIT:
                command += ' --ignore-git'

            check_call(command, shell=True)


def main(args):
    has_jobs = False
    if 'db' in args:
        schedule_database_jobs()
        has_jobs = True
    if 'file' in args:
        schedule_file_jobs()
        has_jobs = True

    if has_jobs:
        # run them all at startup
        for job in schedule.get_jobs():
            job.func()

        if '--run-once' in args:
            return

        try:
            schedule.start()
        except (KeyboardInterrupt, SystemExit):
            pass


if __name__ == '__main__':
    main(sys.argv[1:])
