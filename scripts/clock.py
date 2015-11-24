from __future__ import print_function

from django.core.management import call_command

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
        job_name = fn.__name__
        self.name = job_name
        self.callback = fn
        schedule.add_job(self.run, id=job_name, *self.args, **self.kwargs)
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
        print('Clock job {0}: {1}'.format(self.name, message))


@scheduled_job('interval', minutes=30)
def job_update_externalfiles():
    call_command('update_externalfiles')


@scheduled_job('interval', minutes=30)
def job_update_security_advisories():
    call_command('update_security_advisories')


@scheduled_job('interval', minutes=5)
def job_rnasync():
    call_command('rnasync')


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
    # TODO enable this when we're ready to run a clock process
    # try:
    #     schedule.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass

    # For now just run them all and exit
    for job in schedule.get_jobs():
        try:
            job.func()
        except Exception:
            # exceptions will be printed
            pass
