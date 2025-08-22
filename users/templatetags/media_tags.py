from django import template
from django.conf import settings
from django.templatetags.static import static
import os

register = template.Library()

@register.filter
def media_to_static(media_url):
    """
    Convert media URL to static URL for deployment
    This is a temporary solution for platforms where media files are ephemeral
    """
    if not media_url:
        return static('img/def.jpeg')  # Default avatar
    
    # Remove the /media/ prefix and add /static/media/ prefix
    if media_url.startswith('/media/'):
        static_path = 'media/' + media_url[7:]  # Remove '/media/' and add to static
        return static(static_path)
    elif media_url.startswith('media/'):
        static_path = 'media/' + media_url[6:]  # Remove 'media/' and add to static
        return static(static_path)
    else:
        # If it's already a relative path, just add media/ prefix
        return static('media/' + str(media_url))

@register.simple_tag
def profile_image_url(user):
    """
    Get the profile image URL for a user
    """
    if user and hasattr(user, 'profile_avatar') and user.profile_avatar:
        return media_to_static(user.profile_avatar.url)
    else:
        return static('img/def.jpeg')
