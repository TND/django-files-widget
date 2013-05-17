import os, os.path
from io import FileIO, BufferedWriter
import re
import time

from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from config import *


def make_temp_dir(filename, user):
    now = time.localtime()[0:5]
    dir_name = TEMP_DIR_FORMAT % now
    public_dir = '%s%s/%i/' % (TEMP_DIR, dir_name, user.pk)
    full_dir = '%s%s' % (settings.MEDIA_ROOT, public_dir)

    if not os.path.exists(full_dir):
        os.makedirs(full_dir)

    full_path = '%s%s' % (full_dir, filename)
    available_full_path = default_storage.get_available_name(full_path)
    return available_full_path

def save_upload(uploaded, filename, raw_data, user):
    ''' 
    raw_data: if True, uploaded is an HttpRequest object with the file being
    the raw post data 
    if False, uploaded has been submitted via the basic form
    submission and is a regular Django UploadedFile in request.FILES
    '''

    path = make_temp_dir(filename, user)
    public_path = path.replace(settings.MEDIA_ROOT, '')

    #try:
    with BufferedWriter(FileIO(path, "wb")) as dest:
        # if the "advanced" upload, read directly from the HTTP request 
        # with the Django 1.3 functionality
        if raw_data:
            foo = uploaded.read(1024)
            while foo:
                dest.write(foo)
                foo = uploaded.read(1024) 
        # if not raw, it was a form upload so read in the normal Django chunks fashion
        else:
            for c in uploaded.chunks():
                dest.write(c)
        # got through saving the upload, report success
        return public_path
    #except IOError:
        # could not open the file most likely
    #    pass
    return False


def make_permanent_dir(temp_path, obj):
    model_dir = slugify(type(obj)._meta.verbose_name_plural)
    public_dir = '%s%s/%i/' % (FILES_DIR, model_dir, obj.pk)
    filename = re.sub(r'^.+/', '', temp_path)
    full_dir = '%s%s' % (settings.MEDIA_ROOT, public_dir)

    if not os.path.exists(full_dir):
        os.makedirs(full_dir)

    full_path = '%s%s' % (full_dir, filename)
    available_full_path = default_storage.get_available_name(full_path)
    return available_full_path

def move_to_permanent_dir(temp_path, obj):
    if temp_path.startswith('/') or temp_path.find('//') != -1:
        return temp_path, False

    full_path = make_permanent_dir(temp_path, obj)
    public_path = full_path.replace(settings.MEDIA_ROOT, '')
    full_temp_path = '%s%s' % (settings.MEDIA_ROOT, temp_path)
    os.link(full_temp_path, full_path)

    if temp_path.startswith(TEMP_DIR):
        os.remove(full_temp_path)

    return public_path, True

def move_images_to_permanent_dir(sender, instance, **kwargs):
    # Receiver of Django post_save signal.
    # At this point we know that the model instance has been saved into the db.
    from fields import ImagesField
    fields = [field for field in sender._meta.fields if type(field) == ImagesField]

    for field in fields:
        old_value_attr = OLD_VALUE_STR % field.name
        deleted_value_attr = DELETED_VALUE_STR % field.name
        if not hasattr(instance, old_value_attr):
            continue

        old_images = (getattr(instance, old_value_attr) or '').splitlines()
        deleted_images = (getattr(instance, deleted_value_attr) or '').splitlines()
        current_images = (getattr(instance, field.name) or '').splitlines()
        changed = False

        # Delete removed images from disk if they are in our FILES_DIR.
        for img in old_images:
            if img not in current_images and img.startswith(FILES_DIR):
                os.remove('%s%s' % (settings.MEDIA_ROOT, img))
                changed = True

        # hard link images in FILES_DIR if possible and remove them from TEMP_DIR.
        new_images = []
        for img in current_images:
            path, path_changed = move_to_permanent_dir(img, instance)
            new_images.append(path)
            if path_changed:
                changed = True

        if changed:
            setattr(instance, field.name, '\n'.join(new_images))
            delattr(instance, old_value_attr)
            delattr(instance, deleted_value_attr)
            instance.save()
