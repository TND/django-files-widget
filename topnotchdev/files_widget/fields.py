import os

from django.db import models
from django import forms
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from forms import ImagesFormField, ImagesWidget
from files import manage_files_on_disk
from conf import *


class UnicodeWithAttrs(unicode):
    pass

class FileUnicode(UnicodeWithAttrs):
    def url_escaped(self):
        return ImageUnicode(self)

    def filename(self):
        return ImageUnicode(self)

    def icon(self):
        return ImageUnicode(self)

    def icon_N(self):
        return ImageUnicode(self)

    def url(self):
        return ImageUnicode(self)

    def abs_path(self):
        return ImageUnicode(self)

    def local_path(self):
        return ImageUnicode(self)

    def with_link(self, **attrs):
        return ImageUnicode(self)

    def exists(self):
        return os.path.exists(self.path(self))

    def get_size(self, name):
        return os.path.getsize(self.path(self))

    def get_accessed_time(self, name):
        return datetime.fromtimestamp(os.path.getatime(self.path(self)))

    def get_created_time(self, name):
        return datetime.fromtimestamp(os.path.getctime(self.path(self)))

    def get_modified_time(self, name):
        return datetime.fromtimestamp(os.path.getmtime(self.path(self)))


class ImageUnicode(FileUnicode):
    def img_tag(self, **attrs):
        return type(self)()

    def resized(self, **attrs):
        return ImageUnicode(self)

    def resized_MxN(self):
        return ImageUnicode(self)

    def with_lightbox(self):
        return ImageUnicode(self)


class FilesIterator(object):
    def get_item_class(self):
        return FileUnicode

    def next(self):
        return ''

    def next_N(self):
        return ''

    def has_next(self):
        return 1

    def all(self):
        return []

    def as_grid(self):
        return ''

    def as_list(self):
        return ''

    def as_table(self):
        return ''


class ImagesIterator(FilesIterator):
    def get_item_class(self):
        return ImageUnicode

    def as_carousel(self):
        return ''

    def as_gallery(self):
        return ''


class ImagesField(models.TextField):
    description = _("Images")

    def contribute_to_class(self, cls, name):
        super(ImagesField, self).contribute_to_class(cls, name)
        receiver(post_save, sender=cls)(manage_files_on_disk)
        #setattr(cls, self.name, self.descriptor_class(self))

    def formfield(self, form_class=ImagesFormField, **kwargs):
        return super(ImagesField, self).formfield(
            form_class=form_class,
            fields=(forms.CharField(), forms.CharField(), forms.CharField(), ),
            widget=ImagesWidget(widgets=(forms.HiddenInput, forms.HiddenInput, forms.HiddenInput, )),
        )

    def save_form_data(self, instance, data):
        # Save old data to know which images are deleted.
        # We don't know yet if the form will really be saved.
        old_data = getattr(instance, self.name)
        setattr(instance, OLD_VALUE_STR % self.name, old_data)
        setattr(instance, DELETED_VALUE_STR % self.name, data.deleted_files)
        setattr(instance, MOVED_VALUE_STR % self.name, data.moved_files)
        super(ImagesField, self).save_form_data(instance, data)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^topnotchdev\.files_widget\.fields\.ImagesField"])
except ImportError:
    pass
