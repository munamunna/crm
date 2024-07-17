from django.contrib import admin
from django.urls import path,include
from leadstage import views

urlpatterns = [
    path('generallead',views.GeneralView.as_view(),name='generalsettings'),
    path('leadstages/all',views.LeadstagesView.as_view(),name='leadstages'),
    
    path('leadstages/add',views.add_stage,name='leadstages-add'),
    
]