from django.db import models
from django import forms
from base.models import *

def get_upload_path(instance, filename):
    return 'uploads/%s' % filename

class AddNewBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'rating', 'price', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'autocomplete': 'off'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author', 'autocomplete': 'off'}),
            'rating': forms.NumberInput(attrs={'placeholder': 'Rating', 'autocomplete': 'off'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price', 'min': '1', 'autocomplete': 'off'}),
        }
        

# class AddNewBook(forms.Form):
#     title = forms.CharField(max_length=50, widget=forms.TextInput(
#         attrs={'placeholder': 'Title', 'autocomplete': 'off'}))
#     author = forms.CharField(max_length=50, widget=forms.TextInput(
#         attrs={'placeholder': 'Author', 'autocomplete': 'off'}))
#     rating = forms.IntegerField(
#         widget=forms.NumberInput(attrs={'placeholder': 'Rating', 'autocomplete': 'off'}))
#     price = forms.CharField(widget=forms.NumberInput(
#         attrs={'placeholder': 'Price', 'min': '1', 'autocomplete': 'off'}))
#     image = models.ImageField(upload_to='upload/')