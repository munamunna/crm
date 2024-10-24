
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone


from leadstage.models import LeadStage
 
# Create your models here.
class company_details(models.Model):
    company=models.CharField(max_length=40)
    status=models.CharField(max_length=40,blank=True, null=True)
    firstname=models.CharField(max_length=40)
    lastname=models.CharField(max_length=40,blank=True, null=True)

    def __str__(self):
        return self.company
    
    






class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class contact_details(models.Model):
    email = models.CharField(max_length=100,blank=True, null=True)
    mobile = models.CharField(max_length=20,unique=True)
    mobile_country_code = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    

    

    

class bussiness_details(models.Model):
    executive_name=models.CharField(max_length=40,blank=True, null=True,default='none')
    exe_designation=models.CharField(max_length=40,blank=True, null=True)
    source=models.CharField(max_length=40,blank=True, null=True)
    product=models.CharField(max_length=40,blank=True, null=True)
    requirement=models.CharField(max_length=250,blank=True, null=True)
    notes=models.CharField(max_length=250,blank=True, null=True)
    stages=models.ForeignKey(LeadStage,on_delete=models.CASCADE,blank=True, null=True)
    industry_type=models.CharField(max_length=40,blank=True, null=True)
    gst=models.CharField(max_length=40,blank=True, null=True)
    # address=models.CharField(max_length=100,default='Your default address')

    

    def __str__(self):
        return self.executive_name
    
class Designation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  

class Source(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class IndustryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lead(models.Model):
    company_name = models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20)
    mobile_country_code = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    executive_name = models.CharField(max_length=40, blank=True, null=True)
    exe_designation = models.CharField(max_length=40, blank=True, null=True)
    source = models.CharField(max_length=40, blank=True, null=True)
    product = models.CharField(max_length=40, blank=True, null=True)
    requirement = models.CharField(max_length=250, blank=True, null=True)
    notes = models.CharField(max_length=250, blank=True, null=True)
    stages=models.ForeignKey(LeadStage,on_delete=models.CASCADE,blank=True, null=True)
    industry_type = models.CharField(max_length=40, blank=True, null=True)
    gst = models.CharField(max_length=40, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leads',blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    

    def __str__(self):
        return self.company_name




class Taskactivity(models.Model):
    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    author = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE,null=True
    )
    date_created = models.DateTimeField(default=timezone.now) 
    task_title = models.CharField(max_length=30)
    # assigned_to = models.ForeignKey(
    #     get_user_model(), 
    #     on_delete=models.CASCADE,
    #     related_name='assigned_tasks'
    # )
    related_to = models.ForeignKey(Lead, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    priorty = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    task_description = models.CharField(max_length=250,blank=True, null=True)
    attachment = models.FileField(upload_to='task_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')

    def __str__(self):
        return self.task_title


class DeletedTask(models.Model):
    
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # author = models.ForeignKey(
    #     get_user_model(), 
    #     on_delete=models.CASCADE
    # ,blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now) 
    task_title = models.CharField(max_length=30)
    # assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    related_to = models.ForeignKey(Lead, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    priorty = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    task_description = models.CharField(max_length=250,blank=True, null=True)
    attachment = models.FileField(upload_to='task_attachments/', blank=True, null=True)
    

    def __str__(self):
        return self.task_title


class AppointmentActivity(models.Model):
    APPOINTMENT_TYPE_CHOICES = [
        ('MEETING', 'Meeting'),
        ('CALL', 'Call'),
        ('INTERVIEW', 'Interview'),
        ('OTHER', 'Other'),
    ]

    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES)
    description = models.TextField()
    from_date_time = models.DateTimeField()
    to_date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    related_to = models.CharField(max_length=255, blank=True, null=True)
    # attendees = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.appointment_type} on {self.from_date_time} at {self.location}"


class ClockIn(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} clocked in at {self.clock_in_time} and clocked out at {self.clock_out_time}"


class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    task = models.ForeignKey(Taskactivity, on_delete=models.CASCADE, null=True, blank=True)
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True,blank=True)
    follow_up_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Follow-up for {self.lead.company_name} by {self.user.username} on {self.follow_up_date}"