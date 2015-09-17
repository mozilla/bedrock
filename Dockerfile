FROM debian:jessie

WORKDIR /app
EXPOSE 8000
CMD ["./docker/run-prod.sh"]

RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev

RUN apt-get update && \
    apt-get install -y --no-install-recommends python2.7 libpython2.7 gettext build-essential libmysqlclient-dev libxml2-dev libxslt1.1 libxslt1-dev python-dev virtualenv libmemcached-dev nodejs git postgresql-client libpq-dev
RUN update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10

RUN virtualenv venv -p python2.7

COPY ./requirements /app/requirements
# Pin a known to work with peep pip version.
# RUN venv/bin/pip install -r requirements/pip.txt

# Install app
COPY ./bin/peep.py /app/bin/peep.py
RUN venv/bin/python bin/peep.py install -r requirements/dev.txt
RUN venv/bin/python bin/peep.py install -r requirements/prod.txt
RUN venv/bin/python bin/peep.py install -r requirements/docker.txt
COPY . /app

# RUN git rev-parse HEAD > static/revision.txt
RUN venv/bin/python manage.py collectstatic --noinput
RUN venv/bin/python manage.py update_product_details

# Cleanup
RUN apt-get purge -y python-dev build-essential libxml2-dev libxslt1-dev libmemcached-dev
RUN apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log} /usr/share/doc /usr/share/man /tmp/* /var/cache/* /app/.git
RUN find /app -name *.pyc -delete
RUN venv/bin/python docker/softlinkstatic.py

# Change User
RUN chown webdev.webdev -R .
USER webdev
