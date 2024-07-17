from django.contrib import admin

# Register your models here.
from django.contrib import admin


# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .models import UserType

# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'mobile', 'gender', 'user_type', 'date_of_birth', 'country', 'state', 'city', 'department', 'occupation', 'role', 'pincode', 'address', 'reportee')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'first_name', 'last_name', 'mobile', 'gender', 'user_type', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('email', 'first_name', 'last_name', 'is_staff')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)

admin.site.register(CustomUser)
admin.site.register(UserType)


