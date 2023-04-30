from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout', logout, name='logout'),
    path('', main, name='main'),

    path('profile/', profile, name='profile'),
    path('profile/edit/<int:pk>', profile_edit, name='profile_edit'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
    path('genre/<str:pk>', book_genre, name='book_genre'),
    path('price/<str:pk>', book_price, name='book_price'),
    
    path('profile/book-add/', user_book_add, name='user_book_add'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
