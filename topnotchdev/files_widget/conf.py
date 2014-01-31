from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

MEDIA_URL = getattr(settings, 'MEDIA_URL')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
TEMP_DIR = getattr(settings, 'FILES_WIDGET_TEMP_DIR', 'temp/files_widget/')
TEMP_DIR_FORMAT = getattr(settings, 'FILES_WIDGET_TEMP_DIR_FORMAT', '%4d-%02d-%02d-%02d-%02d')
FILES_DIR = getattr(settings, 'FILES_WIDGET_FILES_DIR', 'uploads/files_widget/')
OLD_VALUE_STR = getattr(settings, 'FILES_WIDGET_OLD_VALUE_STR', 'old_%s_value')
DELETED_VALUE_STR = getattr(settings, 'FILES_WIDGET_DELETED_VALUE_STR', 'deleted_%s_value')
MOVED_VALUE_STR = getattr(settings, 'FILES_WIDGET_MOVED_VALUE_STR', 'moved_%s_value')
JQUERY_PATH = getattr(settings, 'FILES_WIDGET_JQUERY_PATH', '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js')
JQUERY_UI_PATH = getattr(settings, 'FILES_WIDGET_JQUERY_UI_PATH', '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js')
USE_FILEBROWSER = getattr(settings, 'FILES_WIDGET_USE_FILEBROWSER', False)
FILEBROWSER_JS_PATH = getattr(settings, 'FILES_WIDGET_FILEBROWSER_JS_PATH', 'filebrowser/js/AddFileBrowser.js')
ADD_IMAGE_BY_URL = getattr(settings, 'FILES_WIDGET_ADD_IMAGE_BY_URL', True)
MAX_FILESIZE = getattr(settings, 'FILES_WIDGET_MAX_FILESIZE', 0)
FILE_TYPES = getattr(settings, 'FILES_WIDGET_FILE_TYPES', None)
USE_TRASH = getattr(settings, 'FILES_WIDGET_USE_TRASH', False)
TRASH_DIR = getattr(settings, 'FILES_WIDGET_TRASH_DIR', 'uploads/trash/files_widget/')

if not len(MEDIA_URL) or not len(MEDIA_ROOT) or not len(TEMP_DIR) or not len(FILES_DIR):
    raise ImproperlyConfigured('MEDIA_URL, MEDIA_ROOT, FILES_WIDGET_TEMP_DIR and FILES_WIDGET_FILES_DIR must not be empty')
if TEMP_DIR == FILES_DIR:
    raise ImproperlyConfigured('FILES_WIDGET_TEMP_DIR and FILES_WIDGET_FILES_DIR must be different')

if not MEDIA_ROOT.endswith('/'):
    MEDIA_ROOT += '/'
