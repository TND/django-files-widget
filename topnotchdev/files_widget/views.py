import json
import re

from sorl.thumbnail import get_thumbnail

from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required

from .files import save_upload
from .controllers import FilePath, ImagePath


def thumbnail_format(path):
    match = re.search(r'\.\w+$', path)
    if match:
        ext = match.group(0)
        if ext.lower() in ['.gif', '.png']:
            return 'PNG'
    return 'JPEG'


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
    try:
        upload = next(iter(request.FILES.values()))
    except StopIteration:
        return HttpResponseBadRequest(json.dumps({
            'success': False,
            'message': _('Error while uploading file.'),
        }))
    filename = upload.name
    
    path_to_file = save_upload(upload, filename, is_raw, request.user)

    if 'preview_size' in request.POST:
        preview_size = request.POST['preview_size']
    else:
        preview_size = '64'

    thumbnail = get_thumbnail(
        path_to_file, geometry_string="%sx%s" % (preview_size, preview_size),
        upscale=False, format=thumbnail_format(path_to_file))

    return HttpResponse(json.dumps({
        'success': True,
        'imagePath': path_to_file,
        'thumbnailPath': thumbnail.url,
    }))


@permission_required('files_widget.can_upload_files')
def thumbnail_url(request):
    if not 'img' in request.GET or not 'preview_size' in request.GET:
        raise Http404
    
    thumbnail_url = ImagePath(request.GET['img']).thumbnail(request.GET['preview_size']).url
    return HttpResponse(thumbnail_url)
