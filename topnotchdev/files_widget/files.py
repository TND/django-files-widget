import os, os.path
import time

from django.utils.functional import cached_property
from django.core.files.storage import default_storage as storage
from django.template.defaultfilters import slugify

from .conf import *


class NewTempFileHandler(object):
    def __init__(self, filename, user):
        self.filename = filename
        self.user = user

    @classmethod
    def get_temp_dir_name(cls, user):
        now = time.localtime()[0:5]
        dir_name = TEMP_DIR_FORMAT % now
        return os.path.join(dir_name, str(user.pk))

    @classmethod
    def construct_temp_path(cls, user):
        return os.path.join(TEMP_DIR, cls.get_temp_dir_name(user))

    @cached_property
    def get_potential_temp_file_path(self):
        dir_name = self.construct_temp_path(self.user)
        return os.path.join(dir_name, self.filename)

    def save_upload(self, uploaded, raw_data):
        if raw_data:
            result = storage.save(self.get_potential_temp_file_path, raw_data)
        else:
            result = storage.save(self.get_potential_temp_file_path, uploaded)
        return result


class FileHandlerBase(object):
    def __init__(self, file_path):
        self.file_path = file_path

    @cached_property
    def file_name(self):
        return os.path.split(self.file_path)[-1]

    @cached_property
    def is_temp_file(self):
        return storage.exists(self.file_path) and self.file_path.startswith(TEMP_DIR)

    @cached_property
    def is_permanent_file(self):
        return storage.exists(self.file_path) and self.file_path.startswith(FILES_DIR)

    @cached_property
    def target_perm_path(self):
        return storage.get_available_name(os.path.join(self.perm_file_dir, self.file_name))

    @cached_property
    def perm_file_dir(self):
        return self.get_perm_file_dir()

    def get_perm_file_dir(self):
        # This is supposed to be used by non-model submission.
        raise NotImplementedError

    def create_full_os_path_target_dir(self):
        # storage api has no move method, we need to create to folder first.
        os.makedirs(storage.path(self.perm_file_dir), exist_ok=True)

    def move_to_permanent_directory(self):
        if self.is_permanent_file:
            return self.file_path, False

        # todo: when does this happen?
        if self.file_path.startswith('/') or self.file_path.find('//') != -1:
            return self.file_path, False

        try:
            self.create_full_os_path_target_dir()
            os.link(storage.path(self.file_path), storage.path(self.target_perm_path))
        except EnvironmentError as e:
            return self.try_to_recover_path()

        if self.is_temp_file:
            try:
                storage.delete(self.file_path)
            except EnvironmentError:
                return self.try_to_recover_path()

        return self.target_perm_path, True

    def try_to_recover_path(self):
        # This happens when errored while trying to move a temp file to a perm file.
        # We do this to link the temp file back.
        if os.path.exists(self.target_perm_path):
            return self.target_perm_path, True
        else:
            return self.file_path, False

    def delete_this_file(self):
        if self.is_permanent_file or self.is_temp_file:
            try:
                storage.delete(self.file_path)
            except EnvironmentError:
                pass


class ModelFileHandler(FileHandlerBase):
    def __init__(self, file_path, instance):
        super(ModelFileHandler, self).__init__(file_path)
        self.instance = instance

    @classmethod
    def model_slug(cls, model):
        return slugify(model._meta.verbose_name_plural)

    def construct_permanent_path(self):
        model_dir = self.model_slug(type(self.instance))
        return os.path.join(FILES_DIR, model_dir, str(self.instance.pk))

    def get_perm_file_dir(self):
        return self.construct_permanent_path()


class FormFileHandler(FileHandlerBase):
    def __init__(self, file_path, user):
        super(FormFileHandler, self).__init__(file_path)
        self.user = user

    def get_perm_file_dir(self):
        assert self.user is not None
        return os.path.join(FILES_DIR, "non_model_form_upload", str(self.user.pk))


def save_upload(uploaded, filename, raw_data, user):
    '''
    raw_data: if True, uploaded is an HttpRequest object with the file being
    the raw post data
    if False, uploaded has been submitted via the basic form
    submission and is a regular Django UploadedFile in request.FILES
    '''

    fhandler = NewTempFileHandler(filename, user)
    return fhandler.save_upload(uploaded, raw_data)


def manage_files_on_disk(sender, instance, **kwargs):
    # Receiver of Django post_save signal.
    # At this point we know that the model instance has been saved into the db.
    from .fields import ImagesField, ImageField
    fields = [field for field in sender._meta.fields if type(field) in [ImagesField, ImageField]]

    for field in fields:
        old_value_attr = OLD_VALUE_STR % field.name
        deleted_value_attr = DELETED_VALUE_STR % field.name
        moved_value_attr = MOVED_VALUE_STR % field.name
        if not hasattr(instance, old_value_attr):
            continue

        old_images = (getattr(instance, old_value_attr) or '').splitlines()
        current_images = (getattr(instance, field.name) or '').splitlines()
        deleted_images = (getattr(instance, deleted_value_attr) or '').splitlines()
        moved_images = (getattr(instance, moved_value_attr) or '').splitlines()
        new_images = []
        changed = False

        # Delete removed images from disk if they are in our FILES_DIR.
        # we implement redundant checks to be absolutely sure that
        # files must be deleted. For example, if a JS error leads to
        # incorrect file lists in the hidden inputs, we reconstruct the old value.
        #
        # O = old_images, C = current_images, D = deleted_images
        #
        # what do we do with files that appear in:
        #
        #   ---  (OK)    do nothing, we don't even know it's name :)
        #   --D  (OK)    if in temp dir or permanent dir of inst: delete from disk
        #   -C-  (OK)    if not in permanent dir of inst, create hard link if possible;
        #                if in temp dir, delete
        #   -CD  (ERROR) show warning message after save
        #   O--  (ERROR) put back in current, show warning message after save
        #   O-D  (OK)    if in temp dir or permanent dir of inst: delete from disk
        #   OC-  (OK)    if not in permanent dir of inst, create hard link if possible;
        #                if in temp dir, delete
        #   OCD  (ERROR) show warning message after save

        print("post_save: current %s; deleted %s; old %s" % (current_images, deleted_images, old_images))

        for img in current_images:
            # OC-, -C-, OCD & -CD
            fhandler = ModelFileHandler(img, instance)
            new_path, path_changed = fhandler.move_to_permanent_directory()
            if path_changed:
                changed = True
            new_images.append(new_path)

        for img in deleted_images:
            if img not in current_images:
                # --D & O-D
                fhandler = ModelFileHandler(img, instance)
                if fhandler.is_temp_file or fhandler.is_permanent_file:
                    fhandler.delete_this_file()

        for img in old_images:
            if img not in current_images and img not in deleted_images and img not in moved_images:
                # O--
                changed = True
                new_images.append(img)

        delattr(instance, old_value_attr)
        delattr(instance, deleted_value_attr)
        delattr(instance, moved_value_attr)
        if changed:
            setattr(instance, field.name, '\n'.join(new_images))
            instance.save()
