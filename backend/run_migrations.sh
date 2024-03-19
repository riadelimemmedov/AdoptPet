#!/bin/sh
APP_NAMES=("users" "user_profile" "pet" "upload" "order" "transaction")

for APP_NAME in "${APP_NAMES[@]}"; do
    # Run makemigrations for specific apps
    echo "$APP_NAME"
    poetry run python manage.py makemigrations "$APP_NAME"
done

# Run makemigrations and migrate without specifying a particular app
poetry run python manage.py makemigrations
# poetry run python manage.py migrate --fake-initial
poetry run python manage.py migrate # If you don't want to show migrations status for each migrate, use --noinput after the migrate command
poetry run python manage.py runserver

# Execute any additional commands passed to the script
exec "$@"
