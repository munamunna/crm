from django.contrib import admin
from .models import Country,State,City,Designation,Source,IndustryType,FollowUp
from customer.models import complaint_registration
# Register your models here.
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Designation)
admin.site.register(Source)
admin.site.register(IndustryType)
admin.site.register(complaint_registration)
admin.site.register(FollowUp)
