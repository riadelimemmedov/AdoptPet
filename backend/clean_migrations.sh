#!/bin/sh
# Define the path to your Django project
# APPS_PATH="C:\Users\riade\OneDrive\Документы\adopt-pet\backend\apps"
# ROOT_ABSTRACT="C:\Users\riade\OneDrive\Документы\adopt-pet\backend\abstract"

APPS_PATH="/mnt/c/Users/riade/OneDrive/Документы/adopt-pet/backend/apps"
ROOT_ABSTRACT="/mnt/c/Users/riade/OneDrive/Документы/adopt-pet/backend/abstract"


# Iterate over each app in the project
for APP_PATH in "$APPS_PATH"/*/; do
    # Get the app name from the path
    APP_NAME=$(basename "$APP_PATH")

    # Delete migrations folder
    MIGRATIONS_PATH="$APP_PATH/migrations"
    if [ -d "$MIGRATIONS_PATH" ]; then
        rm -rf "$MIGRATIONS_PATH"
        echo "Deleted migrations folder for app: $APP_NAME"
    fi

    # Delete __pycache__ folder
    PYCACHE_PATH="$APP_PATH/__pycache__"
    if [ -d "$PYCACHE_PATH" ]; then
        rm -rf "$PYCACHE_PATH"
        echo "Deleted __pycache__ folder for app: $APP_NAME"
    fi
done


#Execute any additional commands passed to the script
MIGRATIONS_PATH_ABSTRACT="$ROOT_ABSTRACT/migrations"
PYCACHE_PATH_ABSTRACT="$ROOT_ABSTRACT/__pycache__"
rm -rf "$MIGRATIONS_PATH_ABSTRACT"
rm -rf "$PYCACHE_PATH_ABSTRACT"

exec "$@"
