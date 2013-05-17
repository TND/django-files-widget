import json

from django.http import Http404, HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required

from util import save_upload


@permission_required('files_widget.can_upload_files')
def upload(request):
    if not request.method == 'POST':
        raise Http404

    if request.is_ajax():
        # the file is stored raw in the request
        upload = request
        is_raw = True
        # AJAX Upload will pass the filename in the querystring if it is the "advanced" ajax upload
        try:
            filename = request.GET['file']
        except KeyError:
            return HttpResponseBadRequest(json.dumps({
                'success': False,
                'message': 'Error while uploading file.',
            }))
    # not an ajax upload, so it was the "basic" iframe version with submission via form
    else:
        is_raw = False
        if len(request.FILES) == 1:
            # FILES is a dictionary in Django but Ajax Upload gives the uploaded file an
            # ID based on a random number, so it cannot be guessed here in the code.
            # Rather than editing Ajax Upload to pass the ID in the querystring,
            # observer that each upload is a separate request,
            # so FILES should only have one entry.
            # Thus, we can just grab the first (and only) value in the dict.
            upload = request.FILES.values()[0]
        else:
            return HttpResponseBadRequest(json.dumps({
                'success': False,
                'message': 'Error while uploading file.',
            }))
        filename = upload.name
    
    path_to_file = save_upload(upload, filename, is_raw, request.user)
    MEDIA_URL = settings.MEDIA_URL

    return HttpResponse(json.dumps({
        'success': True,
        'imagePath': path_to_file,
        'thumbnailPath': render_to_string('files_widget/includes/thumbnail.html', locals()),
    }))

@permission_required('files_widget.can_upload_files')
def thumbnail_url(request):
    if not 'img' in request.GET:
        return Http404
    return HttpResponse(render_to_string('files_widget/includes/thumbnail.html', { 'path_to_file': request.GET['img'] }))
