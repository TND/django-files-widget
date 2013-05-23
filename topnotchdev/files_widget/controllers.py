import re
import urllib
import os, os.path
from datetime import datetime

from django.conf import settings
from django.utils import six
from django.utils.safestring import mark_safe
from django.utils.functional import curry

from sorl.thumbnail import get_thumbnail


class FilePath(unicode):
    def __new__(cls, str, instance, field, settings={}):
        self = super(FilePath, cls).__new__(cls, str.strip())
        self._instance = instance
        self._field = field
        self._exists = None
        self._size = None
        self._accessed_time = None
        self._created_time = None
        self._modified_time = None
        self._thumbnails = {}
        self.settings = {
            'img_attrs': {},
            'thumbnail_size': None,
            'thumbnail_attrs': {},
        }
        self.settings.update(settings)
        return self

    def _html_attrs(self, **kwargs):
        attrs = {}
        attrs.update(kwargs)
        if 'css_class' in attrs:
            attrs['class'] = attrs['css_class']
            del attrs['css_class']
        return attrs

    @property
    def escaped(self):
        return urllib.unquote(self)

    @property
    def url(self):
        if not self.startswith('/') and self.find('//') == -1:
            return '%s%s' % (settings.MEDIA_URL, self.escaped)
        return self.escaped

    @property
    def local_path(self):
        if not self.startswith('/') and self.find('//') == -1:
            return u'%s%s' % (settings.MEDIA_ROOT, self)
        return self

    @property
    def filename(self):
        return urllib.unquote(re.sub(r'^.+\/', '', self))

    @property
    def display_name(self):
        without_extension = re.sub(r'\.[\w\d]+$', '', self.filename)
        with_spaces = re.sub(r'_', ' ', without_extension)
        return with_spaces

    @property
    def ext(self):
        return re.sub(r'^.+\.', '', self.filename)

    def exists(self):
        if self._exists == None:
            self._exists = os.path.exists(self.local_path)
        return self._exists

    def get_size(self):
        if self._size == None:
            self._size = os.path.getsize(self.local_path)
        return self._size

    def get_accessed_time(self):
        if self._accessed_time == None:
            self._accessed_time = datetime.fromtimestamp(os.path.getatime(self.local_path))
        return self._accessed_time

    def get_created_time(self):
        if self._created_time == None:
            self._created_time = datetime.fromtimestamp(os.path.getctime(self.local_path))
        return self._created_time

    def get_modified_time(self):
        if self._modified_time == None:
            self._modified_time = datetime.fromtimestamp(os.path.getmtime(self.local_path))
        return self._modified_time


class ImagePath(FilePath):
    def img_tag(self, **kwargs):
        attrs = {}
        attrs.update(self.settings['img_attrs'])
        attrs.update(kwargs)
        attrs = self._html_attrs(**attrs)
        attrs_str = ''.join([
            u'%s="%s" ' % (key, value)
            for key, value in attrs.items()
        ])
        return mark_safe(u'<img src="%s" %s/>' % (self.url, attrs_str))

    def _thumbnail_file_format(self):
        if self.ext.lower() in ['gif', 'png']:
            return 'PNG'
        return 'JPEG'

    def thumbnail(self, size=None, **kwargs):
        size = size or self.settings['thumbnail_size']
        if not size:
            raise Exception('No thumbnail size supplied')

        attrs = {
            'format': self._thumbnail_file_format(),
            'upscale': False,
        }
        attrs.update(self.settings['thumbnail_attrs'])
        attrs.update(kwargs)

        all_attrs = { 'size': size }
        all_attrs.update(attrs)
        key = hash(frozenset(all_attrs))

        if not key in self._thumbnails:
            try:
                thumbnail = get_thumbnail(self.local_path, size, **attrs)
            except EnvironmentError:
                return ''
            self._thumbnails[key] = thumbnail
        else:
            thumbnail = self._thumbnails[key]

        return thumbnail

    def _thumbnail_mxn(self, size, **kwargs):
        return self.thumbnail(size)

    def thumbnail_tag(self, size, opts={}, **kwargs):
        thumbnail = self.thumbnail(size, **opts)
        src = ImagePath(thumbnail.url, self._instance, self._field)
        attrs = { 'width': thumbnail.width, 'height': thumbnail.height }
        attrs.update(self.settings['img_attrs'])
        attrs.update(kwargs)
        return src.img_tag(**attrs)

    def _thumbnail_tag_mxn(self, size, opts={}, **kwargs):
        return self.thumbnail_tag(size, opts, **kwargs)

    def __getattr__(self, attr):
        thumbnail_mxn = re.match(r'^thumbnail_(tag_)?(\d*x?\d+)$', attr)
        if thumbnail_mxn:
            tag = thumbnail_mxn.group(1) == 'tag_'
            size = thumbnail_mxn.group(2)
            if tag:
                return curry(self._thumbnail_tag_mxn, size)
            else:
                return curry(self._thumbnail_mxn, size)

        raise AttributeError


class FilePaths(unicode):
    item_class = FilePath

    def __new__(cls, str, instance, field, settings={}):
        self = super(FilePaths, cls).__new__(cls, str)
        self._instance = instance
        self._field = field
        self._all = None
        self._length = None
        self._current = 0
        self.settings = {
            'img_attrs': {},
            'thumbnail_size': None,
            'thumbnail_attrs': {},
        }
        self.settings.update(settings)
        return self

    def all(self):
        if self._all == None:
            self._all = []
            for f in self.splitlines():
                self._all.append(self._field.attr_class.item_class(f, self._instance, self._field, self.settings))

            self._length = len(self._all)

        return self._all

    def count(self):
        self.all()
        return self._length

    def first(self):
        return self.all() and self.all()[0] or None

    def last(self):
        return self.all() and self.all()[-1] or None

    def next(self):
        f = self.all()[self._current]
        self._current += 1
        return f

    def next_n(self, n):
        files = self.all()[self._current:self._current+n]
        self._current += n
        return files

    def next_all(self):
        files = self.all()[self._current:]
        self._current = self._length - 1
        return files

    def has_next(self):
        self.all()
        return max(0, self._length - self._current - 1)

    def reset(self):
        self._current = 0

    def __getattr__(self, attr):
        next_n = re.match(r'^next_(\d+)$', attr)
        if next_n:
            n = int(next_n.group(1))
            return curry(self.next_n, n)

        raise AttributeError


class ImagePaths(FilePaths):
    item_class = ImagePath

    def as_gallery(self):
        raise NotImplementedError

    def as_carousel(self):
        raise NotImplementedError


class FilesDescriptor(object):
    """
    Used django.db.models.fields.files.FileDescriptor as an example.
    This descriptor returns an unicode object, with special methods
    for formatting like filename(), absolute(), relative() and img_tag().
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        files = instance.__dict__[self.field.name]
        if isinstance(files, six.string_types) and not isinstance(files, (FilePath, FilePaths, )) or files is None:
            attr = self.field.attr_class(files, instance, self.field)
            instance.__dict__[self.field.name] = attr

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value
