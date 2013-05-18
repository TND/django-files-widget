from django.contrib import admin

from conf import *

# currently not used
class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^my_view/$', self.my_view)
        )
        return my_urls + urls

    def my_view(self, request):
        # custom view which should return an HttpResponse
        pass
