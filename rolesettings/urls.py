from django.contrib import admin
from django.urls import path,include
from rolesettings import views

urlpatterns = [
    # path('generallead',views.GeneralView.as_view(),name='generalsettings'),
    path('roles/all',views.RolesView.as_view(),name='roles'),
    
    path('roles/add',views.add_role,name='roles-add'),
    path('assign-permissions/', views.assign_permissions, name='assign_permissions'),
    path('role/<int:pk>/', views.RoleDetailView.as_view(), name='role_detail'),
    
]