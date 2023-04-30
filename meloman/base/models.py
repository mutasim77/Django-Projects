from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    is_active = models.BooleanField(default=False)
    
    # additionally
    image = models.ImageField(upload_to='users/', null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    fullname = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=70, help_text="The title of the book.")
    image = models.ImageField(upload_to='images/')
    rating = models.IntegerField(help_text="The the reviewer has given.")
    author = models.CharField(max_length=70, help_text="The name of Author")
    price = models.CharField(max_length=10, help_text="Price of book")
    is_published = models.BooleanField(default=False)
    genre = models.CharField(null=True,max_length=70, help_text="The genre of the book.")
    
    def __str__(self):
        return self.title


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, help_text="Enter your desired username", widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'autocomplete': 'off'}))
    password = forms.CharField(max_length=50, help_text="Enter a strong password", widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'autocomplete': 'off'}))
    confirm_password = forms.CharField(max_length=50, help_text="Confirm your password",
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    age = forms.IntegerField(help_text="Enter your age", widget=forms.NumberInput(
        attrs={'placeholder': 'Enter age', 'min': '1'}))
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect, help_text="Select your gender")
    # image = forms.ImageField(help_text="Upload a profile image", widget=forms.ClearableFileInput(attrs={'placeholder': 'Profile image'}))


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Password'}))
