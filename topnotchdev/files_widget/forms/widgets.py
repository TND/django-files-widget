from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from topnotchdev.files_widget.config import *


class ImagesWidget(forms.MultiWidget):
    class Media:
        js = (
            JQUERY_PATH,
            JQUERY_UI_PATH,
            FILEBROWSER_JS_PATH,
            'files_widget/js/jquery.filedrop.js',
            'files_widget/js/widgets.js',
        )
        css = {
            'all': (
                'files_widget/css/widgets.css',
            ),
        }

    def decompress(self, value):
        if value:
            return [value, '', ]
        return ['', '', ]

    def render(self, name, value, attrs=None):
        if not isinstance(value, list):
            value = self.decompress(value)

        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL,
            'input_string': super(ImagesWidget, self).render(name, value, attrs),
            'name': name,
            'files': value[0],
            'deleted_files': value[1],
        }
        return render_to_string("files_widget/images_widget.html", context)
