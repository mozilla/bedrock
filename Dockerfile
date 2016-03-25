from mozorg/bedrock_base

COPY ./node_modules ./
COPY package.json ./
RUN npm install --production

COPY ./requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt
RUN pip install --no-cache-dir -r requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/docker.txt
RUN pip install --no-cache-dir -r requirements/docker-dev.txt

COPY . ./

RUN ./manage.py collectstatic -l -v 0 --noinput

# Cleanup
RUN ./docker/bin/softlinkstatic.py

# Change User
# No USER directive since supervisor is set to run processes as webdev
RUN chown webdev.webdev -R .

CMD ["docker/run-supervisor.sh"]
