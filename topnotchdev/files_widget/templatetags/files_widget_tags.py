import re
from six.moves import urllib

from django import template


register = template.Library()

@register.filter
def thumbnail_format(path):
    match = re.search(r'\.\w+$', path)
    if match:
        ext = match.group(0)
        if ext.lower() in ['.gif', '.png']:
            return 'PNG'
    return 'JPEG'

@register.filter
def filename_from_path(path):
    return re.sub(r'^.+\/', '', path)

@register.filter
def unquote(value):
    "urldecode"
    return urllib.parse.unquote(value)
