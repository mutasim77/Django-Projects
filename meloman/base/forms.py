from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'age', 'gender']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        if not any(char.islower() for char in password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'))
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        age = cleaned_data.get('age')
        gender = cleaned_data.get('gender')

        if password and confirm_password and password != confirm_password:
            raise ValidationError(_("Passwords don't match."))
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('This username is already taken.'))

