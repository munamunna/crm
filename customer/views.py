from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,TemplateView,UpdateView
from .models import Customer,complaint_registration
from .forms import ComplaintRegistrationForm,CustomerChangeForm,ComplaintChangeForm
from employee.models import Employee
from django.contrib import messages
from django.urls import reverse_lazy
import uuid
import random
import string
from .models import Customer
from ticket.models import Ticketss
from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import ComplaintRegistrationForm
from .models import Customer, complaint_registration
from datetime import datetime

import random
import string
from .models import Customer, complaint_registration
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import ComplaintRegistrationForm
from datetime import datetime


# Create your views here.
class CustomerListView(ListView,LoginRequiredMixin):
    model=Customer
    template_name="customerlist.html"
    context_object_name="customers"

    def get_queryset(self):
        queryset = super().get_queryset().filter(author=self.request.user)
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(mobile__icontains=search_query) |
                Q(company_name__icontains=search_query)
            )

        return queryset





# def generate_unique_client_code():
#     while True:
#         code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
#         if not Customer.objects.filter(client_code=code).exists():
#             return code

# class CustomerEmployeeDetailView(TemplateView):
#     template_name = "latestdetail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = ComplaintRegistrationForm()
#         customer_id = self.kwargs.get('customer_id')
#         if customer_id:
#             context['customer'] = Customer.objects.get(id=customer_id)
#         return context

#     def post(self, request, *args, **kwargs):
#         customer_id = self.kwargs.get('customer_id')
#         if customer_id:
#             customer = Customer.objects.get(id=customer_id)
            
#             # Ensure the customer has a client code
#             if not customer.client_code:
#                 customer.client_code = generate_unique_client_code()
#                 customer.save()

#             # Process customer form submission
#             complaintregistration = complaint_registration(
#                 person_type='Client',
#                 requester_name=request.POST.get('requester_name'),
#                 designation=request.POST.get('designation', ''),
#                 phone_number=request.POST.get('phone_number'),
#                 email=request.POST.get('email', ''),
#                 defult_issues=request.POST.get('defult_issues', ''),
#                 complaint=request.POST.get('complaint', '')
#             )

#             # Generate a unique registration number
#             today = datetime.today()
#             date_str = today.strftime('%Y%m%d')
#             count_today = complaint_registration.objects.filter(
#                 registration_number__startswith=f"{customer.client_code}{date_str}"
#             ).count() + 1
#             registration_number = f"{customer.client_code}{date_str}{count_today}"
#             complaintregistration.registration_number = registration_number
#             complaintregistration.save()

#             messages.success(request, f'Complaint registered successfully! Your registration number is {registration_number}.')
#             return redirect('customer_detail', customer_id=customer_id)

#         return render(request, self.template_name, {'form': ComplaintRegistrationForm()})

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.timezone import datetime
from .models import Customer, complaint_registration
from .forms import ComplaintRegistrationForm

def generate_unique_client_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        if not Customer.objects.filter(client_code=code).exists():
            return code


class CustomerEmployeeDetailView(TemplateView):
    template_name = "latestdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComplaintRegistrationForm()
        customer_id = self.kwargs.get('customer_id')
        if customer_id:
            context['customer'] = Customer.objects.get(id=customer_id)
        return context

    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)

            if not customer.client_code:
                customer.client_code = generate_unique_client_code()
                customer.save()
            
            # assign_to_user_id = request.POST.get('assign_to')
            # assign_to_user = CustomUser.objects.get(id=assign_to_user_id)

            person_type = request.POST.get('person_type')

            complaintregistration = complaint_registration(
                person_type=person_type,
                requester_name=request.POST.get('requester_name'),
                designation=request.POST.get('designation', ''),
                phone_number=request.POST.get('phone_number'),
                email=request.POST.get('email', ''),
                defult_issues=request.POST.get('defult_issues', ''),
                complaint=request.POST.get('complaint', ''),
                # assign_to=assign_to_user,
            )

            today = datetime.today()
            date_str = today.strftime('%Y%m%d')
            count_today = complaint_registration.objects.filter(
                registration_number__startswith=f"{customer.client_code}{date_str}"
            ).count() + 1
            registration_number = f"{customer.client_code}{date_str}{count_today}"
            complaintregistration.registration_number = registration_number
            
            complaintregistration.save()

            # Ticketss.objects.create(
            #     registration_number=registration_number,
            #     assign_to=complaintregistration.assign_to,
            #     requester_name=complaintregistration.requester_name,
            #     priority='',
            #     status='open'
            # )

            messages.success(request, f'Complaint registered successfully! Your registration number is {registration_number}.')
            return redirect('customer_detail', customer_id=customer_id)

        return render(request, self.template_name, {'form': ComplaintRegistrationForm()})






class CustomerEditView(UpdateView):
        model=Customer
        form_class=CustomerChangeForm
        template_name="customer-edit.html"
        success_url=reverse_lazy("clist")

        def form_valid(self, form):
            # messages.success(self.request,"changed")
            return super().form_valid(form)


from django.contrib.auth.mixins import LoginRequiredMixin
class ComplaintListView(ListView,LoginRequiredMixin):
    model=complaint_registration
    template_name="complaintlist.html"
    context_object_name="complaints"

  

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticket.models import Ticketss

 # Import your models here
from django.db.models import Q
class AssignedComplaintsListView(LoginRequiredMixin, ListView):
    template_name = 'assigned_complaints1.html'
    context_object_name = 'complaints'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticketss.objects.all()  # Query all tickets
        return context

    def get_queryset(self):
        return complaint_registration.objects.all()  # Query all complaints


   
    

    def get_queryset(self):
        return complaint_registration.objects.filter(
            Q(assign_to=self.request.user) )
        





# class ComplaintEditView(UpdateView):
#     model = complaint_registration
#     form_class = ComplaintChangeForm
#     template_name = "complaint-edit.html"
#     context_object_name = "complaint"

#     def get_success_url(self):
#         return reverse_lazy('complaint_edit', kwargs={'pk': self.object.pk})

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
        
#         return super().form_valid(form)



class ComplaintEditView(UpdateView):
    model = complaint_registration
    form_class = ComplaintChangeForm
    template_name = "complaint-edit.html"
    context_object_name = "complaint"

    def get_success_url(self):
        return reverse_lazy('complaint_edit', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all remarks associated with this complaint, handle empty queryset
        context['remarks'] = self.object.remarks.all() if self.object.remarks.exists() else []
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Optionally add success messages or other logic here
        return super().form_valid(form)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import complaint_registration, ComplaintRemark

@login_required
def add_remark(request, complaint_id):
    complaint = get_object_or_404(complaint_registration, id=complaint_id)
    if request.method == 'POST':
        remark_text = request.POST.get('remark')
        if remark_text:
            ComplaintRemark.objects.create(
                complaint=complaint,
                remark=remark_text,
                author=request.user
            )
    return redirect('complaint_edit', pk=complaint_id)
