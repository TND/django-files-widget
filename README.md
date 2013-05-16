django-files-widget (pre-alpha)
===================

Django model fields and admin widgets for multiple files/images upload

This is currently a pre-alpha release. Not all functionality is there. There is currently no error handling built in at all.

Features
--------

- Drag &amp; drop file uploading via AJAX (using jQuery Filedrop)
- Upload progress bar
- Multiple or single file upload
- 4 model fields with corresponding form fields and widgets: ImagesField, ImageField, FilesField, and FileField
- Uploading multiple files at once
- Image gallery widget with drag &amp; drop reordering (using jQueryUI Sortable)

Quick Start
-----------

### Requirements ###
- (pip install) sorl-thumbnail
- Unix (file saving uses os.link())
- (currently) (pip install) mezzanine; we will remove this requirement before our stable release
- jQuery 1.7 or later
- jQuery UI


Credits
-------

- [jQuery Filedrop 0.1](https://github.com/weixiyen/jquery-filedrop) (forked)
- [Tutorial on jQuery Filedrop](http://tutorialzine.com/2011/09/html5-file-upload-jquery-php/) by Martin Angelov
- [Tutorial on Django AJAX file upload](http://kuhlit.blogspot.nl/2011/04/ajax-file-uploads-and-csrf-in-django-13.html) on KuhlIT
- [Answer on global file permissions](http://stackoverflow.com/questions/13932774/how-can-i-use-django-permissions-without-defining-a-content-type-or-model) on Stackoverflow

