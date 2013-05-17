from django import forms
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as _

from files_widget.forms.widgets import ImagesWidget


class ImagesFormField(forms.MultiValueField):
    def compress(self, data_list):
        return data_list[0]
