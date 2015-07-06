import os

from django.db import models
from django import forms
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .forms import FilesFormField, BaseFilesWidget, FileWidget, FilesWidget, ImageWidget, ImagesWidget
from .files import manage_files_on_disk
from . import controllers
from .conf import *


def formfield_defaults(self, default_widget=None, widget=None, form_class=FilesFormField, required=True, **kwargs):
    if not isinstance(widget, BaseFilesWidget):
        widget = default_widget

    defaults = {
        'form_class': FilesFormField,
        'fields': (forms.CharField(required=required), forms.CharField(required=False), forms.CharField(required=False), ),
        'widget': widget,
    }
    defaults.update(kwargs)

    return defaults

def save_all_data(self, instance, data):
    # Save old data to know which images are deleted.
    # We don't know yet if the form will really be saved.
    old_data = getattr(instance, self.name)
    setattr(instance, OLD_VALUE_STR % self.name, old_data)
    setattr(instance, DELETED_VALUE_STR % self.name, data.deleted_files)
    setattr(instance, MOVED_VALUE_STR % self.name, data.moved_files)


class FileField(models.CharField):
    description = _("File")
    attr_class = controllers.FilePath

    def __init__(self, max_length=200, **kwargs):
        super(FileField, self).__init__(max_length=max_length, **kwargs)

    def contribute_to_class(self, cls, name):
        super(FileField, self).contribute_to_class(cls, name)
        receiver(post_save, sender=cls)(manage_files_on_disk)
        setattr(cls, self.name, controllers.FilesDescriptor(self))

    def save_form_data(self, instance, data):
        save_all_data(self, instance, data)
        super(FileField, self).save_form_data(instance, data)

    def formfield(self, default_widget=FileWidget(), **kwargs):
        defaults = formfield_defaults(self, default_widget, **kwargs)
        return super(FileField, self).formfield(**defaults)


class FilesField(models.TextField):
    description = _("Files")
    attr_class = controllers.FilePaths

    def contribute_to_class(self, cls, name):
        super(FilesField, self).contribute_to_class(cls, name)
        receiver(post_save, sender=cls)(manage_files_on_disk)
        setattr(cls, self.name, controllers.FilesDescriptor(self))

    def save_form_data(self, instance, data):
        save_all_data(self, instance, data)
        super(FilesField, self).save_form_data(instance, data)

    def formfield(self, default_widget=FilesWidget(), **kwargs):
        defaults = formfield_defaults(self, default_widget, **kwargs)
        return super(FilesField, self).formfield(**defaults)


class ImageField(FileField):
    description = _("Image")
    attr_class = controllers.ImagePath

    def formfield(self, default_widget=ImageWidget(), **kwargs):
        defaults = formfield_defaults(self, default_widget, **kwargs)
        return super(ImageField, self).formfield(**defaults)


class ImagesField(FilesField):
    description = _("Images")
    attr_class = controllers.ImagePaths

    def formfield(self, default_widget=ImagesWidget(), **kwargs):
        defaults = formfield_defaults(self, default_widget, **kwargs)
        return super(ImagesField, self).formfield(**defaults)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^topnotchdev\.files_widget\.fields\.FileField"])
    add_introspection_rules([], ["^topnotchdev\.files_widget\.fields\.FilesField"])
    add_introspection_rules([], ["^topnotchdev\.files_widget\.fields\.ImageField"])
    add_introspection_rules([], ["^topnotchdev\.files_widget\.fields\.ImagesField"])
except ImportError:
    pass
