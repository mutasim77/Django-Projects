from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

from base.models import User, Book


# ? Admin login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/admin/users/')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'admin_panel/admin_login.html', {'error_message': error_message})


# ? Admin logout
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


# ? List of all users;
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_panel/user_list.html', {'users': users})


# ? List of all Books;
def book_list(request):
    books = Book.objects.all()
    return render(request, 'admin_panel/book_list.html', {'books': books})


# ? Edit user info
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.password = request.POST.get('password')
        user.age = request.POST.get('age')
        user.gender = request.POST.get('gender')
        user.save()
        return redirect('user_list')
    return render(request, 'admin_panel/user_edit.html', {'user': user})


# ? Delete User from table
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'admin_panel/user_delete.html', {'user': user})


# ? Edit user info
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.image = request.POST.get('image')
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.rating = request.POST.get('rating')
        book.price = request.POST.get('price')
        book.save()
        return redirect('book_list')
    return render(request, 'admin_panel/book_edit.html', {'book': book})


# ? Delete Book from table
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'admin_panel/book_delete.html', {'book': book})


# ? Delete Book from table
def book_add(request):
    if request.method == 'POST':
        form = AddNewBook(request.POST, request.FILES) 
        print('Hello', form)
        if form.is_valid():
            new_book = Book(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                rating=form.cleaned_data['rating'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data['image']
            )
            new_book.save()
            return redirect('book_list')
    else:
        form = AddNewBook()
    return render(request, 'admin_panel/add_new_book.html', {'form': form})
