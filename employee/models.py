from django.db import models



class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

