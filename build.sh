#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)
psql -a -d $DATABASE_URL -f init.sql