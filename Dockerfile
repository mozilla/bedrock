########
# Pinned `uv` binary, copied into the stages that install Python deps.
# Keep in sync with `setup-uv` `version` in the docs workflows.
#
FROM ghcr.io/astral-sh/uv:0.13.4 AS uv


########
# Python dependencies builder
#
FROM python:3.13-slim-bookworm AS python-builder

WORKDIR /app
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT=/venv
# Overrides a local `.python-version` when the repo is mounted in. A version, not a path, so `uv pip` still finds `/venv` first on `PATH`
ENV UV_PYTHON=3.13
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_CACHE=1
ENV UV_COMPILE_BYTECODE=1

COPY docker/bin/apt-install /usr/local/bin/
RUN apt-install ca-certificates build-essential gettext libxml2-dev libxslt1-dev libxslt1.1
COPY --from=uv /uv /usr/local/bin/

COPY pyproject.toml uv.lock ./

# Install Python deps
RUN uv sync --locked --no-default-groups


########
# Lockfile updates for `make compile-requirements`
#
# Kept separate from `python-builder`, whose `uv sync --locked` fails while
# `pyproject.toml` and `uv.lock` disagree, which is exactly when this is needed
#
FROM python:3.13-slim-bookworm AS uv-lock

WORKDIR /app
ENV UV_PYTHON=3.13
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_CACHE=1

COPY --from=uv /uv /usr/local/bin/


########
# assets builder and dev server
#
FROM node:24-slim AS assets

ENV PATH=/app/node_modules/.bin:$PATH
WORKDIR /app

# copy dependency definitions
COPY package.json package-lock.json ./

# install dependencies
RUN npm ci --verbose

# copy supporting files and media
COPY eslint.config.js .stylelintrc .prettierrc.json .prettierignore webpack.config.js webpack.static.config.js ./
COPY ./media ./media
COPY ./tests/unit ./tests/unit

RUN npm run build --verbose


########
# django app container
#
FROM python:3.13-slim-bookworm AS app-base

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
RUN apt-install ca-certificates curl gettext git libmagickwand-dev libpq-dev libxslt1.1 sqlite3

# copy in Python environment
COPY --from=python-builder /venv /venv

# changes infrequently
COPY docker/gitconfig /etc/
COPY ./bin ./bin
COPY ./etc ./etc
COPY ./lib ./lib
COPY ./root_files ./root_files
COPY ./scripts ./scripts
COPY ./wsgi ./wsgi
COPY manage.py LICENSE ./

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
COPY docker/bin/ssllabs-scan /usr/local/bin/ssllabs-scan
ENV UV_PROJECT_ENVIRONMENT=/venv
ENV UV_PYTHON=3.13
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_CACHE=1
ENV UV_COMPILE_BYTECODE=1
COPY --from=uv /uv /usr/local/bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --locked
COPY ./setup.cfg ./
COPY ./.coveragerc ./
COPY ./tests ./tests

RUN bin/run-sync-all.sh

RUN chown webdev:webdev -R .

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

ARG DEMO_SERVER_ADMIN_USERS
ENV DEMO_SERVER_ADMIN_USERS=${DEMO_SERVER_ADMIN_USERS}

RUN bin/run-sync-all.sh

COPY --from=assets /app/assets /app/assets

RUN honcho run --env docker/envfiles/prod.env docker/bin/build_staticfiles.sh

# Change User
RUN chown webdev:webdev -R .
USER webdev

# build args
ARG GIT_SHA=latest
ENV GIT_SHA=${GIT_SHA}

RUN echo "${GIT_SHA}" > ./root_files/revision.txt
