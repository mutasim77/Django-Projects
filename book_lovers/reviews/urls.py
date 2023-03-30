from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('book-search/', book_search, name='book_search')
]
