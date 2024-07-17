from django.contrib import admin
from .models import Country,State,City,Designation,Source,IndustryType

# Register your models here.
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Designation)
admin.site.register(Source)
admin.site.register(IndustryType)
