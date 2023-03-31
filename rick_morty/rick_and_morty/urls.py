from django.contrib import admin
from django.urls import path
from rick.views import cards

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cards)
]
