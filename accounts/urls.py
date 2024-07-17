from django.contrib import admin
from django.urls import path,include
from accounts import views

urlpatterns = [
    
    path('register/',views.create_user,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.sign_out_view,name='logout'),
    path('users/',views.UsersView.as_view(),name='users'),
     path('password/change/',views.PasswordResetView.as_view(),name="password-reset"),
    # path('permission/',views.PermissionlView.as_view(),name='login'),
    # path('permission/',views.submit_permissions,name='login'),
    
   
    
]