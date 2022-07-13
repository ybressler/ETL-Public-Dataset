#!/bin/bash
migrate=false
upgrade=false
erd=false

while getopts m:ur flag
do
    case "${flag}" in
        m) message=${OPTARG} migrate=true;;
        u) upgrade=true;;
        r) erd=true;;
    esac
done


# Make the version directory if it doesn't exist
# mkdir -p database/migrations_manager/alembic/versions

if $migrate; then
  alembic -c database/migrations_manager/alembic.ini revision --autogenerate -m "$message"
fi

if $upgrade; then
  alembic -c database/migrations_manager/alembic.ini upgrade head
fi

if $erd; then
  echo "skipping creation of ERD"
fi
