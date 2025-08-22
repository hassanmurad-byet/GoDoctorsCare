import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.templatetags.static import static
from django.shortcuts import redirect
import mimetypes

@require_GET
@cache_control(max_age=3600)  # Cache for 1 hour
def serve_media(request, path):
    """
    Serve media files in production
    Try media directory first, then fallback to static/media
    """
    # Security check - ensure path doesn't contain '..' to prevent directory traversal
    if '..' in path:
        raise Http404("Invalid path")

    # Try original media directory first
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # If not found in media, try static/media directory
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        static_media_path = os.path.join(settings.BASE_DIR, 'static', 'media', path)
        if os.path.exists(static_media_path) and os.path.isfile(static_media_path):
            file_path = static_media_path
        else:
            # If it's a profile image, try to serve from static/media via redirect
            if 'users/profiles' in path:
                try:
                    static_url = static(f'media/{path}')
                    return redirect(static_url)
                except:
                    pass

            # Default fallback image for profiles
            if 'users/profiles' in path:
                try:
                    default_static_url = static('img/def.jpeg')
                    return redirect(default_static_url)
                except:
                    pass

            raise Http404("File not found")

    # Get mime type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'

    # Read and return file
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            return response
    except IOError:
        raise Http404("File not found")
