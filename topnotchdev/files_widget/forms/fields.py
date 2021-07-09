from django import forms
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as _
import six

from topnotchdev.files_widget.conf import *


class UnicodeWithAttr(six.text_type):
    deleted_files = None
    moved_files = None


class FilesFormField(forms.MultiValueField):
    def __init__(self, max_length=None, multiple=True, preview_size=64, **kwargs):
        from topnotchdev.files_widget.forms.widgets import FilesWidget
        kwargs.update(
            {
                "widget": FilesWidget(
                    multiple=multiple,
                    preview_size=preview_size
                ),
                'fields': (
                   forms.CharField(required=kwargs.get("required")),
                   forms.CharField(required=False),
                   forms.CharField(required=False), ),
            }
        )
        super(FilesFormField, self).__init__(**kwargs)

    def compress(self, data_list):
        files = UnicodeWithAttr(data_list[0])
        files.deleted_files = data_list[1]
        files.moved_files = data_list[2]
        return files

    def clean(self, value):
        """
        This is a copy of MultiValueField.clean() with a BUGFIX:
        -   if self.required and field_value in validators.EMPTY_VALUES:
        +   if field.required and field_value in validators.EMPTY_VALUES:
        """
        from django.forms.utils import ErrorList
        from django.core.exceptions import ValidationError

        clean_data = []
        errors = ErrorList()
        if not value or isinstance(value, (list, tuple)):
            if not value or not [v for v in value if v not in validators.EMPTY_VALUES]:
                if self.required:
                    raise ValidationError(self.error_messages['required'])
                else:
                    return self.compress(value)
        else:
            raise ValidationError(self.error_messages['invalid'])
        for i, field in enumerate(self.fields):
            try:
                field_value = value[i]
            except IndexError:
                field_value = None
            if field.required and field_value in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['required'])
            try:
                clean_data.append(field.clean(field_value))
            except ValidationError as e:
                # Collect all validation errors in a single list, which we'll
                # raise at the end of clean(), rather than raising a single
                # exception for the first error we encounter.
                errors.extend(e.messages)
        if errors:
            raise ValidationError(errors)

        out = self.compress(clean_data)
        self.validate(out)
        self.run_validators(out)
        return out


class FileFormField(FilesFormField):
    def __init__(self, max_length=None, multiple=False, preview_size=128, **kwargs):
        super(FileFormField, self).__init__(
            max_length, multiple, preview_size, **kwargs)


class ImageFormField(FilesFormField):
    def __init__(self, max_length=None, multiple=False, preview_size=258, **kwargs):
        super(ImageFormField, self).__init__(
            max_length, multiple, preview_size, **kwargs)


class ImagesFormField(FilesFormField):
    def __init__(self, max_length=None, multiple=True, preview_size=150, **kwargs):
        super(ImagesFormField, self).__init__(
            max_length, multiple, preview_size, **kwargs)
