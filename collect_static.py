#!/usr/bin/env python
"""
Script to collect static files for deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
    django.setup()
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
