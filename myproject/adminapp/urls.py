from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('admin_home/', views.admin_home_view, name='admin_home'),
    path('admin_logout/', views.admin_logout_view, name='admin_logout'),
    path('admin_create_user/', views.admin_create_user, name='admin_create_user'),
    path('admin_edit_user/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin_delete_user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
]
