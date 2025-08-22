#!/usr/bin/env python
"""
Create sample profile images by copying existing images
"""
import os
import shutil
from pathlib import Path

def create_sample_profiles():
    """Create sample profile images in static/media directory"""
    
    # Paths
    base_dir = Path(__file__).parent
    static_media_profiles = base_dir / 'static' / 'media' / 'users' / 'profiles'
    media_profiles = base_dir / 'media' / 'users' / 'profiles'
    static_img = base_dir / 'static' / 'img'
    
    # Create directories
    static_media_profiles.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating sample profile images...")
    print(f"Static media profiles: {static_media_profiles}")
    print(f"Media profiles: {media_profiles}")
    
    # Copy from media to static/media if media exists
    if media_profiles.exists():
        print("Copying from media directory...")
        for file_path in media_profiles.glob('*'):
            if file_path.is_file():
                dest_path = static_media_profiles / file_path.name
                try:
                    shutil.copy2(file_path, dest_path)
                    print(f"✓ Copied: {file_path.name}")
                except Exception as e:
                    print(f"✗ Error copying {file_path.name}: {e}")
    
    # Create some default profile images using existing static images
    default_images = [
        'def.jpeg',
        'logo.png',
    ]
    
    sample_names = [
        'doctor1.jpg',
        'doctor2.jpg', 
        'doctor3.jpg',
        'patient1.jpg',
        'patient2.jpg'
    ]
    
    for i, sample_name in enumerate(sample_names):
        source_img = static_img / default_images[i % len(default_images)]
        dest_img = static_media_profiles / sample_name
        
        if source_img.exists() and not dest_img.exists():
            try:
                shutil.copy2(source_img, dest_img)
                print(f"✓ Created sample: {sample_name}")
            except Exception as e:
                print(f"✗ Error creating {sample_name}: {e}")
    
    # List what we have
    print(f"\nFiles in {static_media_profiles}:")
    if static_media_profiles.exists():
        for file_path in static_media_profiles.glob('*'):
            if file_path.is_file():
                print(f"  - {file_path.name}")
    else:
        print("  (directory does not exist)")

if __name__ == '__main__':
    create_sample_profiles()
