FROM python:3.9.10-slim-bullseye

# Run all security updates
# add Postgres dependencies
# Keep apt tidy for container size
RUN apt update && apt upgrade -y && \
  apt install -y libpq-dev build-essential netcat && \
  apt autoremove && apt clean

RUN mkdir -p /opt/api

COPY api /opt/api

WORKDIR /opt/api

RUN pip install -U pip && \
  pip install -r requirements.txt && \
  pip cache purge

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]