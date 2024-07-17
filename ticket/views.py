from django.views.generic import ListView,DetailView,TemplateView,UpdateView
from .models import Ticketss

class TicketListView(ListView):
    model=Ticketss
    template_name="ticketlist.html"
    context_object_name="tickets"


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.utils import timezone
from datetime import datetime
from .models import Ticketss
from .forms import TicketssForm

# class TicketssCreateView(CreateView):
#     model = Ticketss
#     form_class = TicketssForm
#     template_name = 'ticket-add.html'
#     success_url = reverse_lazy('tickets')  

#     def form_valid(self, form):
      
#         customer = form.cleaned_data['requester_name']
        
      
#         today = datetime.today()
#         date_str = today.strftime('%Y%m%d')
#         count_today = Ticketss.objects.filter(
#             registration_number__startswith=f"{customer.client_code}{date_str}"
#         ).count() + 1
#         registration_number = f"{customer.client_code}{date_str}{count_today}"
#         form.instance.registration_number = registration_number
        
#         return super().form_valid(form)

from django.utils import timezone
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import TicketssForm
from .models import Ticketss
from customer.models import Customer,complaint_registration
from accounts.models import CustomUser

class TicketssCreateView(CreateView):
    model = Ticketss
    form_class = TicketssForm
    template_name = 'ticket-add.html'
    success_url = reverse_lazy('tickets')  # Adjust this URL as needed

    def form_valid(self, form):
        # Get the selected customer from the form
        customer = form.cleaned_data['requester_name']

        # Generate a unique registration number
        today = datetime.today()
        date_str = today.strftime('%Y%m%d')
        count_today = Ticketss.objects.filter(
            registration_number__startswith=f"{customer.client_code}{date_str}"
        ).count() + 1
        registration_number = f"{customer.client_code}{date_str}{count_today}"
        form.instance.registration_number = registration_number
        
        # Save the Ticketss instance
        response = super().form_valid(form)
        
        # Get the assign_to user from the form
        # assign_to_user_id = self.request.POST.get('assign_to')
        # assign_to_user = CustomUser.objects.get(id=assign_to_user_id)

        # Create a new complaint_registration entry
        complaint_registration_instance = complaint_registration(
            date_created=timezone.now(),
            person_type='Admin',  # Or any other appropriate value
            requester_name=form.cleaned_data['requester_name'],
            designation='',  # Fill in with appropriate data if available
            phone_number='',  # Fill in with appropriate data if available
            email='',  # Fill in with appropriate data if available
            defult_issues='',  # Fill in with appropriate data if available
            complaint=form.cleaned_data.get('description', ''),
            registration_number=registration_number,
        #     assign_to=assign_to_user, 
        )
        complaint_registration_instance.save()

        return response

class TicketDetailView(DetailView):
    model = Ticketss
    template_name = "ticket_detail.html"
    context_object_name = "ticket"

class TicketEditView(UpdateView):
        model=Ticketss
        form_class=TicketssForm
        template_name="ticket-edit.html"
        success_url=reverse_lazy("tickets")
        context_object_name = "ticket" 

        def form_valid(self, form):
            # messages.success(self.request,"changed")
            return super().form_valid(form)