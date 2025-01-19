from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

@never_cache
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_home')

    if request.method == 'POST':
        admin_name = request.POST.get('username')
        admin_password = request.POST.get('password')

        user = authenticate(request, username=admin_name, password=admin_password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, 'Invalid admin credentials. Please try again.')
            return redirect('admin_login')

    return render(request, 'admin_login.html')

@never_cache
@login_required
def admin_home_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. You are not a superuser.')
        return redirect('admin_login')

    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(username__icontains=search_query) | User.objects.filter(email__icontains=search_query)
    else:
        users = User.objects.all()

    return render(request, 'admin_home.html', {'users': users, 'search_query': search_query})

@never_cache
@login_required
def admin_logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')

@never_cache
@login_required
def admin_create_user(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. You are not a superuser.')
        return redirect('admin_login')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if username and email and password:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'User  created successfully.')
            return redirect('admin_home')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'admin_create_user.html')

@never_cache
@login_required
def admin_edit_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. You are not admin')
        return redirect('admin_login')

    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'User  updated successfully.')
        return redirect('admin_home')
    
    return render(request, 'admin_edit_user.html', {'user': user})

@never_cache
@login_required
def admin_delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. You are not a superuser.')
        return redirect('admin_login')

    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User  deleted successfully.')
    return redirect('admin_home')