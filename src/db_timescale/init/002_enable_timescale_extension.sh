#!/bin/bash
set -e

# add this script for extra safety in case extension is not enabled by default

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
EOSQL