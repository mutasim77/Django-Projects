from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout', logout, name='logout'),
    path('', main, name='main'),

    path('profile/', profile, name='profile'),
    path('cart/', cart, name='cart'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
]
