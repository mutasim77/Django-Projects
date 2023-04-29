from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    # User
    path('admin/', admin_login, name='admin_login'),
    path('admin/', admin_logout, name='admin_logout'),
    path('admin/users/', user_list, name='user_list'),
    path('admin/user-edit/<int:pk>', user_edit, name='user_edit'),
    path('admin/user-delete/<int:pk>', user_delete, name='user_delete'),

    # Book
    path('admin/books/', book_list, name='book_list'),
    path('admin/book-add/', book_add, name='book_add'),
    path('admin/book-edit/<int:pk>', book_edit, name='book_edit'),
    path('admin/book-delete/<int:pk>', book_delete, name='book_delete'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
