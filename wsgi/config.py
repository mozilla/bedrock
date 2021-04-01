# see http://docs.gunicorn.org/en/latest/configure.html#configuration-file

from os import getenv

from prometheus_client import multiprocess


bind = f'0.0.0.0:{getenv("PORT", "8000")}'
workers = getenv('WEB_CONCURRENCY', 2)
accesslog = '-'
errorlog = '-'
loglevel = getenv('LOGLEVEL', 'info')

# Larger keep-alive values maybe needed when directly talking to ELBs
# See https://github.com/benoitc/gunicorn/issues/1194
keepalive = getenv('WSGI_KEEP_ALIVE', 2)
worker_class = getenv('GUNICORN_WORKER_CLASS', 'meinheld.gmeinheld.MeinheldWorker')
worker_tmp_dir = '/dev/shm'


# see https://github.com/prometheus/client_python#multiprocess-mode-gunicorn
def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)
