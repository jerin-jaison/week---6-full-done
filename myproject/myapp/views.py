from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
def signup_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        username = name 

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
    
        user = User.objects.create_user(username=username, password=password)
        user.email = email  
        user.save()
        messages.success(request, 'Signup successful!')
        return redirect('login')

    return render(request, 'signup.html')

@login_required
@never_cache
def home_view(request): 
    return render(request, 'home.html', {'user': request.user})

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password.' 
            return render(request, 'login.html', {'error_message': error_message})  
    return render(request, 'login.html')

@never_cache
def signout_view(request):
    logout(request)
    return redirect('login')