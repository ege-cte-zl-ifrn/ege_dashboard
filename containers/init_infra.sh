#!/bin/bash
#
# Perform required tasks to setup the infraestructure components.

source env.sh

echo_info "Starting db..."
docker-compose up -d db
until docker-compose run db psql -h db -U postgres -c '\l' >/dev/null 2>&1; do
  echo_warning "Postgres is unavailable - sleeping"; sleep 1
done

for s in "${SCHEMAS[@]}"; do
  echo_info "Creating schema $s..."
  docker-compose run db psql -q -h db -U postgres -c "CREATE SCHEMA IF NOT EXISTS $s;"
done