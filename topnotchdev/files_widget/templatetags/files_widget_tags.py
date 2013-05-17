import re
from django import template


register = template.Library()

@register.filter
def thumbnail_format(filename):
    match = re.search(r'\.\w+$', filename)
    if match:
        ext = match.group(0)
        if ext.lower() in ['.gif', '.png']:
            return 'PNG'
    return 'JPEG'

@register.filter
def filename_from_path(path):
    return re.sub(r'^.+\/', '', path)
