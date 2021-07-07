import re
from six.moves import urllib

from django import template


register = template.Library()

@register.filter
def filename_from_path(path):
    return re.sub(r'^.+\/', '', path)

@register.filter
def unquote(value):
    "urldecode"
    return urllib.parse.unquote(value)
