from django.contrib import admin
from django.urls import path,include
from ticket import views

urlpatterns = [
    # path('generallead',views.GeneralView.as_view(),name='generalsettings'),
    path('tickets/all',views.TicketListView.as_view(),name='tickets'),
    path('tickets/add/', views.TicketssCreateView.as_view(), name='tickets_create'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/change', views.TicketEditView.as_view(), name='ticket_edit'),
    
    # path('departments/add',views.add_department,name='departments-add'),
    
]