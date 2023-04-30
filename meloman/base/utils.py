import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User

def validate_form_data(username, password, confirm_password, age, gender):
    errors = {}
    
    # Empty fields
    if not (username and password and confirm_password and age and gender):
        errors['empty_fields'] = 'All fields are required!'

    # Less than 8 characters password error(register)
    if len(password) < 8:
        errors['short_password'] = 'Password should have at least 8 characters!'

    # Minimum one upper case and one lower case and one number should contain password
    if not (re.search('[a-z]', password) and re.search('[A-Z]', password) and re.search('[0-9]', password)):
        errors['weak_password'] = 'Password should contain at least one upper case letter, one lower case letter, and one number!'

    # Check if passwords match
    if password != confirm_password:
        errors['password_mismatch'] = 'Passwords do not match!'

    #  Username shouldn’t be duplicated.
    user = User.objects.filter(username=username)
    if user:
        errors['existing_username'] = 'Username already exists!'

    return errors


