from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name