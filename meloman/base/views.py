from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from hashlib import sha256
from django.urls import reverse
import os
from django.conf import settings

from .models import *
from .utils import validate_form_data
import sys
from admin_panel.models import AddNewBook

# ? MAIN PAGE
def main(request):
    data_id = request.session.get('data_id')
    if data_id is not None:
        try:
            data = User.objects.get(id=data_id)
            context = {'data': data}
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            context = {}
    else:
        context = {}

    books = Book.objects.filter(is_published=True)
    context['books'] = books
    
    search_input = request.GET.get('search') or ''   
    if search_input:
        context['books'] = context['books'].filter(title__icontains=search_input)
        context['flag'] = 'Flag'
        
    return render(request, 'base/main.html', context)

    
#? REGISTER USER
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        password_hash = sha256(password.encode()).hexdigest()
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # Validate form data
        errors = validate_form_data(username, password, confirm_password, age, gender)
        if errors:
            error_message = list(errors.values())[-1]
            messages.add_message(request, messages.ERROR, error_message)
            return redirect('register')

        obj = User()
        obj.username = username
        obj.password = password_hash
        obj.age = age
        obj.gender = gender
        obj.save()
        messages.success(request, 'Registration successful!')
        return redirect('login_user')
    else:
        response = render(request, 'base/register.html')
        response['Cache-Control'] = 'no-cache'
        return response


# ? LOGIN USER
def login_user(request):
    context = {}
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            password_hash = sha256(password.encode()).hexdigest()
            data = User.objects.get(username=username, password=password_hash)
            
            # #if user is not active
            # if not data.is_active:
            #     print('hello', data, data.is_active)
            #     context['error'] = "Username is not active"
            #     return redirect('login_user')
            
            if data is not None:
                request.session['data_id'] = data.id
                return redirect(reverse('main'))
            
        except Exception as e:
            context['error'] = "Invalid username or password"

    return render(request, 'base/login.html', context)

# ? LOGOUT USER
def logout(request):
    request.session.flush()
    return redirect('login_user')


# ? BLOG
def blog(request):
    return render(request, 'base/blog.html')

# ? CONTACT
def contact(request):
    return render(request, 'base/contact.html')

# ? PROFILE
def profile(request):
    user = get_object_or_404(User, id=1)
    return render(request, 'base/profile.html', {'user': user})

# ? Edit user info
def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.age = request.POST.get('age')
        # user.gender = request.POST.get('gender')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.fullname = request.POST.get('fullname')
        
        hash_password = sha256((request.POST.get('password')).encode()).hexdigest() 
        user.password = hash_password
        
        image_file = request.FILES.get('image')
        if image_file:
            # Remove old image if exists
            if user.image:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(user.image)))
            
            # Save new image to media folder
            user.image = image_file
            
        user.save()
        return redirect('profile')
    return render(request, 'base/profile_edit.html', {'user': user})
    
    
    

# ? Add Book to the table
def user_book_add(request):
    if request.method == 'POST':
        form = AddNewBook(request.POST, request.FILES) 
        if form.is_valid():
            new_book = Book(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                rating=form.cleaned_data['rating'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data['image'],
                is_published = False
            )
            new_book.save()
            return redirect('profile')
    else:
        form = AddNewBook()
    return render(request, 'base/user_add_book.html', {'form': form})