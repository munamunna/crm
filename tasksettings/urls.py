from django.contrib import admin
from django.urls import path,include
from tasksettings import views

urlpatterns = [
    path('general',views.GeneralView.as_view(),name='generalsettings'),
    path('taskstages/all',views.TaskstagesView.as_view(),name='taskstages'),
    # path('taskstages/add',views.AddTaskstagesView.as_view(),name='taskstages-add'),
    path('taskstages/add',views.add_stage,name='taskstages-add'),
    
]