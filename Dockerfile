from mozorg/bedrock_base

RUN apt-get install -y --no-install-recommends npm

COPY . /app

RUN npm install --production
RUN pip install --no-cache-dir -r requirements/dev.txt
RUN pip install --no-cache-dir -r requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/docker.txt

RUN ./manage.py collectstatic -l --noinput

# Cleanup
RUN ./docker/bin/softlinkstatic.py

# Shallow clone l10n repo into locale
RUN bash -c "if [[ ! -e locale ]]; then git clone --depth 1 https://github.com/mozilla-l10n/bedrock-l10n locale; fi"

# Change User
RUN chown webdev.webdev -R .
USER webdev
