
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
