FROM python:2.7-slim as base

ARG BRANCH_NAME=master
ENV BRANCH_NAME=$BRANCH_NAME
ARG GIT_SHA=testing
ENV GIT_SHA=$GIT_SHA

# from https://github.com/mozmeao/docker-pythode/blob/master/Dockerfile.footer

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# add non-priviledged user
RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev

# Add apt script
COPY docker/bin/apt-install /usr/local/bin/

# end from Dockerfile.footer

WORKDIR /app
EXPOSE 8000
CMD ["./bin/run.sh"]

RUN apt-install gettext build-essential libxml2-dev libxslt1.1 libxslt1-dev git libpq-dev

COPY ./requirements ./requirements

# Install Python deps
RUN pip install --no-cache-dir -r requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/docker.txt


FROM base as builder

### from the official nodejs dockerfile ###
# https://github.com/nodejs/docker-node/blob/master/6.11/slim/Dockerfile

# gpg keys listed at https://github.com/nodejs/node#release-team
RUN set -ex \
  && for key in \
  9554F04D7259F04124DE6B476D5A82AC7E37093B \
  94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
  FD3A5288F042B6850C66B31F09FE44734EB7990E \
  71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
  DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
  B9AE9905FFD7803F25714661B63B535A4C206CA9 \
  C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
  56730D5401028683275BD23C23EFEFE93C4CFFFE \
  ; do \
  gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$key" || \
  gpg --keyserver pgp.mit.edu --recv-keys "$key" || \
  gpg --keyserver keyserver.pgp.com --recv-keys "$key" ; \
  done

ENV NPM_CONFIG_LOGLEVEL info
ENV NODE_VERSION 6.11.4

RUN buildDeps='xz-utils' \
  && ARCH= && dpkgArch="$(dpkg --print-architecture)" \
  && case "${dpkgArch##*-}" in \
  amd64) ARCH='x64';; \
  ppc64el) ARCH='ppc64le';; \
  s390x) ARCH='s390x';; \
  arm64) ARCH='arm64';; \
  armhf) ARCH='armv7l';; \
  *) echo "unsupported architecture"; exit 1 ;; \
  esac \
  && set -x \
  && apt-get update && apt-get install -y curl $buildDeps --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
  && curl -SLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
  && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-$ARCH.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
  && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 \
  && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
  && apt-get purge -y --auto-remove $buildDeps \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs

ENV YARN_VERSION 1.1.0

RUN set -ex \
  && for key in \
  6A010C5166006599AA17F08146C2130DFD2497F5 \
  ; do \
  gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$key" || \
  gpg --keyserver pgp.mit.edu --recv-keys "$key" || \
  gpg --keyserver keyserver.pgp.com --recv-keys "$key" ; \
  done \
  && curl -fSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz" \
  && curl -fSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz.asc" \
  && gpg --batch --verify yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz \
  && mkdir -p /opt/yarn \
  && tar -xzf yarn-v$YARN_VERSION.tar.gz -C /opt/yarn --strip-components=1 \
  && ln -s /opt/yarn/bin/yarn /usr/local/bin/yarn \
  && ln -s /opt/yarn/bin/yarn /usr/local/bin/yarnpkg \
  && rm yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz

### End official Node image ###

ENV PATH=/tmp/node_modules/.bin:$PATH
ENV PIPELINE_LESS_BINARY=lessc
ENV PIPELINE_SASS_BINARY=node-sass
ENV PIPELINE_UGLIFYJS_BINARY=uglifyjs
ENV PIPELINE_CLEANCSS_BINARY=cleancss
ENV NODE_ENV=production

COPY package.json yarn.lock /tmp/
RUN cd /tmp && yarn install --pure-lockfile && rm -rf /usr/local/share/.cache/yarn

COPY . ./
RUN docker/bin/build_staticfiles.sh
RUN echo "${GIT_SHA}" > static/revision.txt

# load the code
FROM base

# changes infrequently
COPY ./bin ./bin
COPY ./etc ./etc
COPY ./lib ./lib
COPY ./root_files ./root_files
COPY ./scripts ./scripts
COPY ./wsgi ./wsgi
COPY manage.py LICENSE newrelic.ini contribute.json ./

# changes more frequently
COPY ./docker ./docker
COPY ./vendor-local ./vendor-local
COPY ./bedrock ./bedrock
COPY ./media ./media
COPY --from=builder /app/static ./static

RUN bin/sync-all.sh

# Change User
RUN chown webdev.webdev -R .
USER webdev
