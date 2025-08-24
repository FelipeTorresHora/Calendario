#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip3 install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --no-input

# Run database migrations
python3 manage.py migrate