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
from django.db.models import Count
from django.db.models import Q

from .models import *
from .utils import validate_form_data
import sys
from admin_panel.models import AddNewBook

# ? MAIN PAGE
def main(request):
    context = {}
    data_id = request.session.get('data_id')
    if data_id is not None:
        data = User.objects.get(id=data_id)
        context['data'] = data

    #all books
    books = Book.objects.filter(is_published=True)
    context['books'] = books
    #genre list
    genre_list = sorted(Book.objects.values('genre').annotate(num_books=Count('id')), key=lambda x: x['genre'])
    context['genre_list'] = genre_list
        
    search_input = request.GET.get('search') or ''
    search_results = Book.objects.none()
    last_viewed = Book.objects.none()
    
    if search_input:
        search_results = Book.objects.filter(title__icontains=search_input)
        context['books'] = search_results
        context['flag'] = 'Flag'
        
        search_history = request.session.get('search_history', [])
        if search_history:
            last_viewed = Book.objects.filter(title__icontains=search_history[-1])
            
        search_history.append(search_input)
        search_history = search_history[-5:]
        request.session['search_history'] = search_history
    
    context['last_viewed'] = last_viewed

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
def profile(request, pk):        
    user = get_object_or_404(User, id=pk)
    return render(request, 'base/profile.html', {'user': user})

# ? Edit user info
def profile_edit(request, pk):
    user = get_object_or_404(User, id=pk)
    print("Hello", user)
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
            if user.image:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(user.image)))

            user.image = image_file
            
        user.save()
        return redirect('profile', pk=pk)
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
                is_published = False,
                genre=form.cleaned_data['genre']
            )
            new_book.save()
            return redirect('/')
    else:
        form = AddNewBook()
    return render(request, 'base/user_add_book.html', {'form': form})


def book_genre(request, pk):
    books = Book.objects.filter(genre__icontains=pk)
    return render(request, 'base/genres.html', {'books' : books})


def book_price(request, pk):
    pk = pk.split('_')
    books = Book.objects.filter(price__gte=pk[0], price__lte=pk[1])
    return render(request, 'base/price.html', {'books' : books})

