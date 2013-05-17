from django import forms
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as _

from topnotchdev.files_widget.config import *
from widgets import ImagesWidget


class UnicodeWithAttr(unicode):
    deleted_files = None

class ImagesFormField(forms.MultiValueField):
    def compress(self, data_list):
        files = UnicodeWithAttr(data_list[0])
        files.deleted_files = data_list[1]
        return files
