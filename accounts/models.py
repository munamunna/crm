from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from crmapp.models import State,City,Country
from departmentsettings.models import Department
from occupationsettings.models import Occupation
from rolesettings.models import Role
from employee.models import Employee


class UserType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name
    
class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    user_type = models.ForeignKey(UserType,on_delete=models.CASCADE, blank=True, null=True)
    

    
    date_of_birth = models.DateField(null=True, blank=True)
    
    country = models.ForeignKey(Country,on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, blank=True, null=True)
    occupation = models.ForeignKey(Occupation,on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE, blank=True, null=True, related_name='customuser')
    
    pincode = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    reportee = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True)
    profile_pic=models.ImageField(upload_to="profilepics",blank=True,default="/profilepics/deafault.jpg")
    

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile', 'gender']

    def __str__(self):
        return self.email

    @property
    def is_manager(self):
        return self.role.name == 'Manager'