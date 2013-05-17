django-files-widget
===================

Django model fields and (admin) form widgets for multiple files/images upload

__This is currently a pre-alpha release. Not all functionality is there, only `ImagesField` has been implemented. There is currently no error handling built in at all.__

Features
--------

- Drag &amp; drop file uploading via AJAX
- Uploading multiple files at once
- Upload progress bar
- Multiple or single file upload
- Four model fields with corresponding form fields and widgets: `ImagesField`, `ImageField`, `FilesField`, and `FileField`
- Image gallery widget with drag &amp; drop reordering
- File list widget with file type icons and metadata

Quick Start
-----------

### Requirements ###
- Django 1.5 or later
- (pip install) sorl-thumbnail
- Unix (file saving uses `os.link()`)
- (currently) (pip install) mezzanine; we will remove this requirement before our stable release
- jQuery 1.7 or later
- jQuery UI

### In `settings.py` ###

    INSTALLED_APPS = (
        ...,
        "files_widget",
        ...,
    )
    
    # basic settings with their defaults
    FILES_WIDGET_TEMP_DIR = 'temp/files_widget/'        # inside MEDIA_ROOT
    FILES_WIDGET_FILES_DIR = 'uploads/files_widget/'    # inside MEDIA_ROOT
    FILES_WIDGET_JQUERY_PATH = ...
    FILES_WIDGET_JQUERY_UI_PATH = ...

### In `urls.py` ###

    ("^files-widget/", include("files_widget.urls")),

### In `models.py` ###

    from files_widget import ImagesField
  
    class MyModel(models.Model):
        images = ImagesField()

### Django Auth user permissions ###

    files_widget.can_upload_files

Credits
-------

- [jQuery Filedrop 0.1](https://github.com/weixiyen/jquery-filedrop) (forked)
- [Tutorial on jQuery Filedrop](http://tutorialzine.com/2011/09/html5-file-upload-jquery-php/) by Martin Angelov
- [Tutorial on Django AJAX file upload](http://kuhlit.blogspot.nl/2011/04/ajax-file-uploads-and-csrf-in-django-13.html) by Alex Kuhl
- [Answer on non-Model user permissions](http://stackoverflow.com/questions/13932774/how-can-i-use-django-permissions-without-defining-a-content-type-or-model) on Stackoverflow

