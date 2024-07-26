from django.contrib import admin
from django.urls import path,include
from departmentsettings import views

urlpatterns = [
   
    path('departments/all',views.DepartmentsView.as_view(),name='departments'),
    
    path('departments/add',views.add_department,name='departments-add'),
    
]