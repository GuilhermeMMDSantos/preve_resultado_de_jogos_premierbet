#!/bin/sh

set -e

export POSTGRES_PASSWORD = "cat $("$POSTGRES_PASSWORD_FILE")"

exec dbt "$@"