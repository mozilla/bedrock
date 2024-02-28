# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# see http://docs.gunicorn.org/en/latest/configure.html#configuration-file

from os import getenv

bind = f"0.0.0.0:{getenv('PORT', 8000)}"
workers = getenv("WEB_CONCURRENCY", 2)
accesslog = "-"
errorlog = "-"
loglevel = getenv("LOGLEVEL", "info")

worker_class = getenv("GUNICORN_WORKER_CLASS", "gevent")
worker_connections = int(getenv("WSGI_WORKER_CONNECTIONS", 1000))
worker_tmp_dir = "/dev/shm"

# Larger keep-alive values maybe needed when directly talking to ELBs
# See https://github.com/benoitc/gunicorn/issues/1194
keepalive = int(getenv("WSGI_KEEP_ALIVE", 60))
timeout = int(getenv("WSGI_TIMEOUT", 30))
graceful_timeout = int(getenv("WSGI_GRACEFUL_TIMEOUT", 10))
max_requests = getenv("WSGI_MAX_REQUESTS", 1300)
max_requests_jitter = getenv("WSGI_MAX_REQUESTS_JITTER", 30)
reuse_port = getenv("WSGI_REUSE_PORT", True)


# Called just after a worker has been forked.
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)
