from django.contrib import admin
from django.urls import path,include
from occupationsettings import views

urlpatterns = [
    # path('generallead',views.GeneralView.as_view(),name='generalsettings'),
    path('occupations/all',views.OccupationView.as_view(),name='occupations'),
    
    path('occupations/add',views.add_occupation,name='occupation-add'),
    
]