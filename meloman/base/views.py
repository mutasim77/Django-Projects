from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from hashlib import sha256
from django.urls import reverse, reverse_lazy
import os
from django.conf import settings
from django.db.models import Count
from django.db.models import Q
from django.views import View
from django.views.generic.edit import CreateView
from .models import *
from .utils import validate_form_data
import sys
from admin_panel.models import AddNewBook


#? REGISTER USER
class RegisterView(View):
    def get(self, request):
        response = render(request, 'base/register.html')
        response['Cache-Control'] = 'no-cache'
        return response
    
    def post(self, request):
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

# ? LOGIN USER
class LoginUserView(View):
    def get(self, request):
        context = {}
        return render(request, 'base/login.html', context)
    
    def post(self, request):
        context = {}
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


#*----------Profile User----------

# ? PROFILE
class ProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return render(request, 'base/profile.html', {'user': user})
    
# ? Edit user info
class ProfileEditView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return render(request, 'base/profile_edit.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        user.username = request.POST.get('username')
        user.age = request.POST.get('age')
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
    
# ? User Add Book
class UserBookAddView(CreateView):
    model = Book
    form_class = AddNewBook
    template_name = 'base/user_add_book.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.is_published = False
        return super().form_valid(form)
    
#? Logout User
class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('login_user')

    
#*----------Views----------

#? Book genres
class BookGenreView(View):
    def get(self, request, pk):
        books = Book.objects.filter(genre__icontains=pk)
        return render(request, 'base/genres.html', {'books' : books})
    
#? Book Price
class BookPriceView(View):
    def get(self, request, pk):
        pk = pk.split('_')
        books = Book.objects.filter(price__gte=pk[0], price__lte=pk[1])
        return render(request, 'base/price.html', {'books': books})

#? Blog
class BlogView(View):
    def get(self, request):
        return render(request, 'base/blog.html')

#? Contact
class ContactView(View):
    def get(self, request):
        return render(request, 'base/contact.html')


# ? MAIN
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
    
    # seach-area;
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
    