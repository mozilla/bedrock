# see http://docs.gunicorn.org/en/latest/configure.html#configuration-file

from os import getenv
from multiprocessing import cpu_count


bind = f'0.0.0.0:{getenv("PORT", "8000")}'

try:
    cpu = cpu_count() * 2 + 1
    workers = getenv("WEB_CONCURRENCY", cpu)
except NotImplementedError:
    workers = 3

accesslog = "-"
errorlog = "-"
loglevel = getenv("LOGLEVEL", "info")

# Larger keep-alive values maybe needed when directly talking to ELBs
# See https://github.com/benoitc/gunicorn/issues/1194
keepalive = getenv("WSGI_KEEP_ALIVE", 118)
worker_class = getenv("GUNICORN_WORKER_CLASS", "meinheld.gmeinheld.MeinheldWorker")
worker_connections = getenv("APP_GUNICORN_WORKER_CONNECTIONS", "1000")
worker_tmp_dir = "/dev/shm"


# Called just after a worker has been forked.
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)
