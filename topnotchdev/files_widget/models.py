from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from .fields import ImageField


class GlobalPermissionManager(models.Manager):
    def get_query_set(self):
        return super(GlobalPermissionManager, self).\
            get_query_set().filter(content_type__name='global_permission')


class GlobalPermission(Permission):
    """A global permission, not attached to a model"""

    objects = GlobalPermissionManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        ct, created = ContentType.objects.get_or_create(
            name="global_permission", app_label=self._meta.app_label
        )
        self.content_type = ct
        super(GlobalPermission, self).save(*args, **kwargs)


try:
    permission = GlobalPermission.objects.get_or_create(
        codename='can_upload_files',
        name='Can Upload Files',
    )
except:
    # "Table 'fileswidgettest16.auth_permission' doesn't exist"
    # it should exist the next time that this file is loaded
    pass


class IconSet(models.Model):
    name = models.CharField(max_length=50, unique=True)
    css_path = models.CharField(max_length=200, blank=True, null=True, help_text='Optional css file for icon styling')
    active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    default_icon = models.ForeignKey('files_widget.FileIcon', null=True, blank=True)


class FileIcon(models.Model):
    icon_set = models.ForeignKey('files_widget.IconSet')
    extension = models.CharField(max_length=100, blank=True, null=True)
    image = ImageField()
    display_text_overlay = models.BooleanField(default=True)
    overlay_text = models.CharField(max_length=7, blank=True, null=True, help_text='Leave blank to display file extension')
    base_color = models.CharField(max_length=12, blank=True, null=True)
