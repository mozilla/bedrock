FROM python:2.7-slim

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
                   && rm -rf /var/lib/apt/lists/*

WORKDIR /home/linkchecker/app
ENV HOME /home/linkchecker
CMD ["./run-linkchecker.sh"]
RUN useradd -ms /bin/bash linkchecker

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./run-linkchecker.sh ./
RUN chown -R linkchecker:linkchecker /home/linkchecker
RUN mkdir /results && chown -R linkchecker:linkchecker /results
USER linkchecker
