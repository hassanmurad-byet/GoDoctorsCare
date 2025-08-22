#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Copy media files to static directory (temporary solution for Render)
python manage.py copy_media

# Create sample profile images
python create_sample_profiles.py

# Collect static files (after copying media)
python manage.py collectstatic --no-input --clear

# Ensure media directory exists
mkdir -p media/users/profiles
