from django.db import models
from django.conf import settings


class Ticketss(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('assigned', 'assigned'),
        
        ('in_progress', 'In Progress'),
        ('pending', 'pending'),
        ('resolved', 'resolved'),

        ('closed', 'Closed'),
    )

    registration_number = models.CharField(max_length=50, unique=True)
    requester_name = models.CharField(max_length=50, blank=True, null=True)
    assign_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    description=models.TextField(blank=True, null=True)
    # Define other fields as required

    def __str__(self):
        return self.registration_number

