from django.shortcuts import render,redirect
from django.views.generic import ListView,TemplateView
from .models import Employee
from customer.models import Customer
from customer.forms import ComplaintRegistrationForm
from employee.models import Employee
from django.contrib import messages
from customer.models import complaint_registration

# Create your views here.
class EmployeeListView(ListView):
    model=Employee
    template_name="employeelist.html"
    context_object_name="employees"

class EmployeeCustomerDetailView(TemplateView):
    template_name = "latedetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs.get('employee_id')
        
        

        if employee_id:
            context['employee'] = Employee.objects.get(id=employee_id)
       

        return context

    def post(self, request, *args, **kwargs):
        
        employee_id = self.kwargs.get('employee_id')

        if employee_id:
            # Process customer form submission
            complaintregistration = complaint_registration(
                person_type='Employee',
                requester_name=request.POST.get('requester_name'),
                designation=request.POST.get('designation', ''),
                phone_number=request.POST.get('phone_number'),
                email=request.POST.get('email', ''),
                defult_issues=request.POST.get('defult_issues', ''),
                complaint=request.POST.get('complaint', '')
            )
            complaintregistration.save()
            messages.success(request, 'Complaint registered successfully!')
            return redirect('employee_detail', employee_id=employee_id)
        
            