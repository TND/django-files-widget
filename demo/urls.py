from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from demo.demo_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
        [path('admin/', admin.site.urls),
         url(r'^files-widget/', include('topnotchdev.files_widget.urls')),
         url(r"^$", views.ImagesWidgetCreateView.as_view(), name="demo-create"),
         url(r"demo2$", views.ImagesWidgetTwoFieldsCreateView.as_view(), name="demo2-create"),
         path("update/<int:pk>", views.ImagesWidgetUpdateView.as_view(), name="demo-update"),
         path("update2/<int:pk>", views.ImagesWidgetTwoFieldsUpdateView.as_view(), name="demo2-update"),
         path("generic", views.Demo3GenericView.as_view(), name="demo3")


         ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
           + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
