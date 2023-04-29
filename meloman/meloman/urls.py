from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('admin_panel.urls')),
]
