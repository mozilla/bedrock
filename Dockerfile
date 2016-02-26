from mozorg/bedrock_base

COPY ./requirements /app/requirements

# Install app
COPY ./bin/peep.py /app/bin/peep.py
RUN ./bin/peep.py install --no-cache-dir -r requirements/dev.txt
RUN ./bin/peep.py install --no-cache-dir -r requirements/prod.txt
RUN ./bin/peep.py install --no-cache-dir -r requirements/docker.txt

COPY . /app

RUN ./manage.py collectstatic -l --noinput

# Cleanup
RUN ./docker/bin/softlinkstatic.py

# Shallow clone l10n repo into locale
RUN bash -c "if [[ ! -e locale ]]; then git clone --depth 1 https://github.com/mozilla-l10n/bedrock-l10n locale; fi"

# Change User
RUN chown webdev.webdev -R .
USER webdev
