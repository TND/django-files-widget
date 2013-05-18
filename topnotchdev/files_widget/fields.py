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


class ImagesField(models.TextField):
    description = _("Images")

    def contribute_to_class(self, cls, name):
        receiver(post_save, sender=cls)(manage_files_on_disk)
        super(ImagesField, self).contribute_to_class(cls, name)

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
