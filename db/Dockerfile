FROM postgres:16-bookworm
RUN apt-get update && apt-get -y install postgresql-16-cron && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY 00-init-schema.sql /docker-entrypoint-initdb.d/    
COPY 01-init-pg_cron.sql /docker-entrypoint-initdb.d/
COPY 02-init-cron-jobs.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
