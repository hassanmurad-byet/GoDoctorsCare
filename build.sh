#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Copy media files to static directory (temporary solution for Render)
python copy_media_to_static.py

# Collect static files (after migrations)
python manage.py collectstatic --no-input --clear

# Ensure media directory exists
mkdir -p media/users/profiles
