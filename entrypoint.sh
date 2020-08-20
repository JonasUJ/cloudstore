#!/bin/sh

# If you are getting an error containing "standard_init_linux.go:211"
# change the line endings of this file from CRLF to LF

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec "$@"
