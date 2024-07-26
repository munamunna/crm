"""
URL configuration for crmproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from crmapp import views
from customer import views as cviews
from employee import views as eviews
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.IndexView.as_view(),name="index"),
    path('index2/',views.IndeView.as_view(),name="index2"),
    path('maindash/',views.mainDashView.as_view(),name="maindash"),
    path('dash/',views.DashView.as_view(),name="dash"),
    path('clock-in/', views.clock_in, name='clock_in'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('user_presence/', views.user_presence, name='user_presence'),
    
    path('leads/add/',views.EnterLeadView.as_view(),name="lead_form"),
    path('leadscount/',views.lead_counts_view,name="lead_count"),
    
    
    path('leads/all/',views.LeadListView.as_view(),name="list"),
    path('tasks/all/',views.TaskListView.as_view(),name="tasklist"),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/remove',views.task_delete_view,name="task-delete"),
    path('appointments/all/',views.AppointmentListView.as_view(),name="appointmentlist"),
    path('lead/<int:pk>/change', views.LeadEditView.as_view(), name='lead_edit'),
    path('lead/<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('dtasks/all/',views.DeletedTaskListView.as_view(),name="dtasklist"),
    path('start-task/<int:pk>/', views.start_task_view, name='start-task'),
    path('complete-task/<int:pk>/', views.complete_task_view, name='complete-task'),
    
    path('convert-lead-to-customer/<int:lead_id>/', views.convert_lead_to_customer, name='convert-lead-to-customer'),
    path('customers/all/',cviews.CustomerListView.as_view(),name="clist"),
    path('customer/<int:pk>/change', cviews.CustomerEditView.as_view(), name='customer_edit'),
    path('complaints/all/',cviews.ComplaintListView.as_view(),name="complaintlist"),
     path('assigned-complaints/',cviews. AssignedComplaintsListView.as_view(), name='assigned_complaints'),
    path('complaints/<int:pk>/change', cviews.ComplaintEditView.as_view(), name='complaint_edit'),
    path('complaints/<int:complaint_id>/add_remark/', cviews.add_remark, name='add_remark'),
    path('employees/all/',eviews.EmployeeListView.as_view(),name="elist"),
    
    path('customer_employee/<int:customer_id>/', cviews.CustomerEmployeeDetailView.as_view(), name='customer_detail'),
    path('employee_customer/<int:employee_id>/', eviews.EmployeeCustomerDetailView.as_view(), name='employee_detail'),
    
    path('',include('tasksettings.urls')),
    path('',include('leadstage.urls')),
    path('',include('rolesettings.urls')),
    path('',include('departmentsettings.urls')),
    path('',include('occupationsettings.urls')),
    path('',include('accounts.urls')),
    path('',include('ticket.urls')),
    

    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)