from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from django.db import models
from crmapp.models import Country, State, City
from employee.models import Employee
from django.utils import timezone
from ticket.models import Ticketss
from accounts.models import CustomUser

from django.conf import settings


class Customer(models.Model):
    company_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20)
    mobile_country_code = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    executive_name = models.ForeignKey(Employee,on_delete=models.CASCADE, blank=True, null=True)
    exe_designation = models.CharField(max_length=40, blank=True, null=True)
    source = models.CharField(max_length=40, blank=True, null=True)
    product = models.CharField(max_length=40, blank=True, null=True)
    requirement = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    stages = models.CharField(max_length=40, blank=True, null=True)
    industry_type = models.CharField(max_length=40, blank=True, null=True)
    gst = models.CharField(max_length=40, blank=True, null=True)
    client_code = models.CharField(max_length=4, unique=True, blank=True, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.company_name


class complaint_registration(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('assigned', 'assigned'),
        
        ('in_progress', 'In Progress'),
        ('pending', 'pending'),
        ('resolved', 'resolved'),

        ('closed', 'Closed'),
    )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    date_created = models.DateTimeField(default=timezone.now)
    person_type=models.CharField(max_length=30)
    requester_name=models.CharField(max_length=40)
    designation=models.CharField(max_length=40,blank=True, null=True)
    phone_number=models.CharField(max_length=40)
    email=models.CharField(max_length=40,blank=True, null=True)
    defult_issues=models.CharField(max_length=40)
    complaint=models.TextField(blank=True, null=True)
    registration_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    assign_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
   
    
    
    

    def __str__(self):
        return f"{self.requester_name}"

  # Adjust the import based on your project structure

class ComplaintRemark(models.Model):
    complaint = models.ForeignKey(complaint_registration, on_delete=models.CASCADE, related_name='remarks')
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Remark on {self.complaint.title}: {self.remark}"
