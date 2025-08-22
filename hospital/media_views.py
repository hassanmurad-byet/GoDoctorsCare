import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
import mimetypes

@require_GET
@cache_control(max_age=3600)  # Cache for 1 hour
def serve_media(request, path):
    """
    Serve media files in production
    """
    # Security check - ensure path doesn't contain '..' to prevent directory traversal
    if '..' in path:
        raise Http404("Invalid path")
    
    # Construct full file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Check if file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
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
