from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', main, name='main'),

    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='profile_edit'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('genre/<str:pk>', BookGenreView.as_view(), name='book_genre'),
    path('price/<str:pk>', BookPriceView.as_view(), name='book_price'),
    
    path('profile/book-add/', UserBookAddView.as_view(), name='user_book_add'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
