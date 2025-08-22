#!/usr/bin/env python
"""
Copy media files to static directory for deployment
This is a temporary solution for platforms like Render where media files are ephemeral
"""
import os
import shutil
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

def copy_media_to_static():
    """Copy media files to static directory"""
    media_root = settings.MEDIA_ROOT
    static_root = os.path.join(settings.BASE_DIR, 'static')

    # Create destination directory
    static_media_dir = os.path.join(static_root, 'media')
    os.makedirs(static_media_dir, exist_ok=True)

    print(f"Media root: {media_root}")
    print(f"Static root: {static_root}")
    print(f"Static media dir: {static_media_dir}")

    # Copy media files to static
    if os.path.exists(media_root):
        print(f"Copying media files from {media_root} to {static_media_dir}")

        # Copy all files and directories
        for root, dirs, files in os.walk(media_root):
            # Calculate relative path
            rel_path = os.path.relpath(root, media_root)
            if rel_path == '.':
                dest_dir = static_media_dir
            else:
                dest_dir = os.path.join(static_media_dir, rel_path)

            # Create destination directory
            os.makedirs(dest_dir, exist_ok=True)
            print(f"Created directory: {dest_dir}")

            # Copy files
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)

                try:
                    shutil.copy2(src_file, dest_file)
                    print(f"✓ Copied: {os.path.basename(src_file)}")
                except Exception as e:
                    print(f"✗ Error copying {src_file}: {e}")

        print("✓ Media files copied to static directory")

        # List what was copied
        if os.path.exists(static_media_dir):
            print("\nFiles in static/media:")
            for root, dirs, files in os.walk(static_media_dir):
                level = root.replace(static_media_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")
    else:
        print(f"✗ Media directory {media_root} does not exist")
        print("Creating empty media structure...")
        os.makedirs(os.path.join(static_media_dir, 'users', 'profiles'), exist_ok=True)
        print("✓ Created static/media/users/profiles directory")

if __name__ == '__main__':
    copy_media_to_static()
