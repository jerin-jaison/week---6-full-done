from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  
    path('login/', views.login_view, name='login'), 
    path('home/', views.home_view, name='home'),
    path('signout/', views.signout_view, name='signout'),  
    path('signup/', views.signup_view, name='signup'), 
    path('signup/login/', views.login_view, name='login'), 
    path('accounts/login/',views.login_view, name='login')
]
