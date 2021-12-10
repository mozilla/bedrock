########
# assets builder and dev server
#
FROM node:17-slim AS assets

ENV PATH=/app/node_modules/.bin:$PATH
WORKDIR /app

# copy dependency definitions
COPY package.json package-lock.json ./

# install dependencies
RUN npm ci

# copy supporting files and media
COPY .eslintrc.js .eslintignore .stylelintrc .prettierrc.json .prettierignore webpack.config.js webpack.static.config.js ./
COPY ./media ./media
COPY ./tests/unit ./tests/unit

RUN npm run build


########
# Python dependencies builder
#
FROM python:3.7-slim-buster AS python-builder

WORKDIR /app
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

COPY docker/bin/apt-install /usr/local/bin/
RUN apt-install gettext build-essential libxml2-dev libxslt1-dev libxslt1.1
RUN python -m venv /venv

COPY requirements/base.txt requirements/prod.txt ./requirements/

# Install Python deps
RUN pip install --no-cache-dir -r requirements/prod.txt


########
# django app container
#
FROM python:3.7-slim-buster AS app-base

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/venv/bin:$PATH"

# add non-priviledged user
RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev

WORKDIR /app
EXPOSE 8000
CMD ["./bin/run.sh"]

COPY docker/bin/apt-install /usr/local/bin/
RUN apt-install gettext libxslt1.1 git curl

# copy in Python environment
COPY --from=python-builder /venv /venv

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
COPY ./bedrock ./bedrock
COPY ./l10n ./l10n
COPY ./media ./media


########
# expanded webapp image for testing and dev
#
FROM app-base AS devapp

CMD ["./bin/run-tests.sh"]

RUN apt-install make
COPY requirements/base.txt requirements/dev.txt requirements/migration.txt requirements/docs.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt
RUN pip install --no-cache-dir -r requirements/docs.txt
COPY ./setup.cfg ./
COPY ./pyproject.toml ./
COPY ./.coveragerc ./
COPY ./tests ./tests

RUN bin/run-sync-all.sh

RUN chown webdev.webdev -R .

# for bpython
RUN mkdir /home/webdev/
RUN touch /home/webdev/.pythonhist
RUN chown -R webdev /home/webdev/

USER webdev

# build args
ARG GIT_SHA=latest
ENV GIT_SHA=${GIT_SHA}


########
# final image for deployment
#
FROM app-base AS release

RUN bin/run-sync-all.sh

COPY --from=assets /app/assets /app/assets

RUN honcho run --env docker/envfiles/prod.env docker/bin/build_staticfiles.sh

RUN echo "${GIT_SHA}" > ./root_files/revision.txt

# Change User
RUN chown webdev.webdev -R .
USER webdev

# build args
ARG GIT_SHA=latest
ENV GIT_SHA=${GIT_SHA}
