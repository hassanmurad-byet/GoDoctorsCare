#!/usr/bin/env python
"""
Test script to check static files configuration
"""
import os
import django
from django.conf import settings
from django.contrib.staticfiles import finders

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

def test_static_files():
    print("=== Static Files Configuration Test ===")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    
    # Test finding specific files
    test_files = [
        'css/bootstrap.min.css',
        'css/style.css',
        'css/front-page.css',
        'js/bootstrap.bundle.min.js',
        'img/godoctor-icon.png'
    ]
    
    print("\n=== Testing Static File Discovery ===")
    for file_path in test_files:
        found = finders.find(file_path)
        if found:
            print(f"✓ Found: {file_path} -> {found}")
        else:
            print(f"✗ Missing: {file_path}")
    
    # Check if static root exists and has files
    print(f"\n=== Static Root Directory ===")
    if os.path.exists(settings.STATIC_ROOT):
        files = os.listdir(settings.STATIC_ROOT)
        print(f"✓ STATIC_ROOT exists with {len(files)} items")
        if 'css' in files:
            css_files = os.listdir(os.path.join(settings.STATIC_ROOT, 'css'))
            print(f"  CSS files: {len(css_files)} files")
    else:
        print("✗ STATIC_ROOT does not exist - run collectstatic")

if __name__ == '__main__':
    test_static_files()
