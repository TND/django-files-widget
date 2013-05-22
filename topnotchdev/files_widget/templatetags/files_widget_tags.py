import re
import urllib

from django import template

from topnotchdev.files_widget.controllers import thumbnail_format


register = template.Library()

register.filter(thumbnail_format)

@register.filter
def filename_from_path(path):
    return re.sub(r'^.+\/', '', path)

@register.filter
def unquote(value):
    "urldecode"
    return urllib.unquote(value)
