import json

from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required
from django.utils import six

from .files import save_upload
from .controllers import FilePath, ImagePath

@permission_required('files_widget.can_upload_files')
def upload(request):
    if not request.method == 'POST':
        raise Http404

    # if request.is_ajax():
    #     # the file is stored raw in the request
    #     upload = request
    #     is_raw = True
    #     # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
    #     try:
    #         filename = request.GET['files[0]']
    #     except KeyError:
    #         return HttpResponseBadRequest(json.dumps({
    #             'success': False,
    #             'message': 'Error while uploading file',
    #         }))
    # not an ajax upload, so it was the "basic" iframe version with submission via form
    # else:
    is_raw = False
    if len(request.FILES) == 1:
        values = request.FILES.values()
        upload = next(values) if six.PY3 else values[0]
    else:
        return HttpResponseBadRequest(json.dumps({
            'success': False,
            'message': 'Error while uploading file.',
        }))
    filename = upload.name
    
    path_to_file = save_upload(upload, filename, is_raw, request.user)
    MEDIA_URL = settings.MEDIA_URL

    if 'preview_size' in request.POST:
        preview_size = request.POST['preview_size']
    else:
        preview_size = '64'

    return HttpResponse(json.dumps({
        'success': True,
        'imagePath': path_to_file,
        'thumbnailPath': render_to_string('files_widget/includes/thumbnail.html', locals()),
    }))

@permission_required('files_widget.can_upload_files')
def thumbnail_url(request):
    if not 'img' in request.GET or not 'preview_size' in request.GET:
        raise Http404
    
    thumbnail_url = ImagePath(request.GET['img']).thumbnail(request.GET['preview_size']).url
    return HttpResponse(thumbnail_url)
