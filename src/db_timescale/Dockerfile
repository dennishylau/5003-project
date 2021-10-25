FROM timescale/timescaledb:latest-pg12

COPY init/* /docker-entrypoint-initdb.d/

RUN chmod -R 755 /docker-entrypoint-initdb.d/