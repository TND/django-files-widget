from builtins import str
from builtins import object
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from topnotchdev.files_widget.conf import *


def use_filebrowser():
    if USE_FILEBROWSER:
        try:
            import filebrowser
            return True
        except:
            try:
                import filebrowser_safe
                return True
            except:
                pass
            pass
    return False

class BaseFilesWidget(forms.MultiWidget):
    def __init__(self,
            multiple=False,
            preview_size=150,
            template="files_widget/files_widget.html",
            widgets=(forms.HiddenInput, forms.HiddenInput, forms.HiddenInput, ),
            **kwargs):
        super(BaseFilesWidget, self).__init__(widgets, **kwargs)
        self.multiple = multiple
        self.preview_size = preview_size
        self.template = template

    class Media:
        js = [
            JQUERY_PATH,
            JQUERY_UI_PATH,
            'files_widget/js/jquery.iframe-transport.js',
            'files_widget/js/jquery.fileupload.js',
            'files_widget/js/widgets.js',
        ]
        if use_filebrowser():
            js.append(FILEBROWSER_JS_PATH)

        css = {
            'all': (
                'files_widget/css/widgets.css',
            ),
        }

    def decompress(self, value):
        if value:
            return [value, '', '', ]
        return ['', '', '', ]

    def render(self, name, value, attrs=None):
        if not isinstance(value, list):
            value = self.decompress(value)
        files, deleted_files, moved_files = value

        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL,
            'use_filebrowser': use_filebrowser(),
            'add_image_by_url': ADD_IMAGE_BY_URL,
            'input_string': super(BaseFilesWidget, self).render(name, value, attrs),
            'name': name,
            'files': files,
            'deleted_files': deleted_files,
            'multiple': self.multiple and 1 or 0,
            'preview_size': str(self.preview_size),
        }
        return render_to_string(self.template, context)


class FileWidget(BaseFilesWidget):
    def __init__(self, multiple=False, preview_size=128, **kwargs):
        super(FileWidget, self).__init__(multiple, preview_size, **kwargs)


class FilesWidget(BaseFilesWidget):
    def __init__(self, multiple=True, preview_size=64, **kwargs):
        super(FilesWidget, self).__init__(multiple, preview_size, **kwargs)


class ImageWidget(BaseFilesWidget):
    def __init__(self, multiple=False, preview_size=250, **kwargs):
        super(ImageWidget, self).__init__(multiple, preview_size, **kwargs)


class ImagesWidget(BaseFilesWidget):
    def __init__(self, multiple=True, preview_size=150, **kwargs):
        super(ImagesWidget, self).__init__(multiple, preview_size, **kwargs)
