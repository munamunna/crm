from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def update_user_permissions(sender, instance, **kwargs):
    if instance.role:
        role_permissions = instance.role.permissions.all()
        instance.user_permissions.set(role_permissions)