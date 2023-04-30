from django.db import models
from django import forms
from base.models import *


class AddNewBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'rating', 'price', 'image', 'is_published', 'genre']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'autocomplete': 'off'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author', 'autocomplete': 'off'}),
            'rating': forms.NumberInput(attrs={'placeholder': 'Rating', 'autocomplete': 'off'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price', 'min': '1', 'autocomplete': 'off'}),
            'genre': forms.TextInput(attrs={'placeholder': 'Genre'})
        }
        
        labels = {
            'is_published': 'Publish this book'
        }