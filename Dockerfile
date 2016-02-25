from mozorg/bedrock_base

COPY . /app

RUN ./manage.py collectstatic -l --noinput

# Cleanup
RUN ./docker/bin/softlinkstatic.py

# Shallow clone l10n repo into locale
RUN bash -c "if [[ ! -e locale ]]; then git clone --depth 1 https://github.com/mozilla-l10n/bedrock-l10n locale; fi"

# Change User
RUN chown webdev.webdev -R .
USER webdev
