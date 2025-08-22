from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Copy media files to static directory for deployment'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        static_root = os.path.join(settings.BASE_DIR, 'static')
        static_media_dir = os.path.join(static_root, 'media')
        
        # Create destination directory
        os.makedirs(static_media_dir, exist_ok=True)
        
        self.stdout.write(f"Media root: {media_root}")
        self.stdout.write(f"Static media dir: {static_media_dir}")
        
        if os.path.exists(media_root):
            self.stdout.write(f"Copying media files...")
            
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
                
                # Copy files
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_dir, file)
                    
                    try:
                        shutil.copy2(src_file, dest_file)
                        self.stdout.write(f"✓ Copied: {file}")
                    except Exception as e:
                        self.stdout.write(f"✗ Error copying {file}: {e}")
            
            self.stdout.write(self.style.SUCCESS("✓ Media files copied to static directory"))
        else:
            self.stdout.write(self.style.WARNING(f"Media directory {media_root} does not exist"))
            # Create empty structure
            os.makedirs(os.path.join(static_media_dir, 'users', 'profiles'), exist_ok=True)
            self.stdout.write("Created empty media structure")
