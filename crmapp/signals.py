
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Lead, contact_details, bussiness_details, company_details

@receiver(pre_save, sender=Lead)
def update_related_details(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Lead.objects.get(pk=instance.pk)
        
        # Update contact_details
        contacts = contact_details.objects.filter(id=old_instance.id)
        for contact in contacts:
            contact.mobile = instance.mobile
            contact.mobile_country_code = instance.mobile_country_code
            contact.email = instance.email
            contact.country = instance.country
            contact.state = instance.state
            contact.city = instance.city
            contact.save()

        # Update bussiness_details
        business = bussiness_details.objects.filter(id=old_instance.id)
        for bus in business:
            bus.executive_name = instance.executive_name
            bus.exe_designation = instance.exe_designation
            bus.source = instance.source
            bus.product = instance.product
            bus.requirement = instance.requirement
            bus.notes = instance.notes
            bus.industry_type = instance.industry_type
            bus.gst = instance.gst
            bus.save()

        # Update company_details
        companies = company_details.objects.filter(id=old_instance.id)
        for company in companies:
            company.company = instance.company_name
            company.firstname = instance.first_name
           
            company.save()

