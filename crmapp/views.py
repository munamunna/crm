from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,UpdateView,ListView,DetailView
from .forms import  CompanyDetailsForm, ContactDetailsForm, BusinessDetailsForm,LeadChangeForm,TaskActivityForm
from .models import contact_details,bussiness_details,company_details,Taskactivity
from django.utils.decorators import method_decorator
from employee.models import Employee
from django.db import connection
from django.db.models import Q
from django.db.models import Count

from .models import contact_details, bussiness_details, company_details,Lead,Employee, AppointmentActivity
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404, redirect
from customer.models import Customer
from django.urls import reverse_lazy
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.decorators import role_required,signin_required
from django.contrib import messages

from django.views.generic import DetailView,ListView
from django.shortcuts import render
from django.utils import timezone


from .models import Taskactivity,DeletedTask
from customer.models import complaint_registration 
 




# Create your views here.
# @method_decorator(role_required('admin'), name='dispatch')
# @method_decorator(signin_required,name="dispatch")


from django.utils import timezone

class mainDashView(TemplateView):
    template_name = "maindashboard.html"

class DashView(TemplateView):
    template_name = "dashboard.html"

class IndexView(TemplateView):
    template_name = "index1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_count'] = Customer.objects.count()
        context['user_count'] = CustomUser.objects.count()
        context['complaint_count'] = complaint_registration.objects.count()
        
        # Add the count of overdue tasks
        overdue_tasks_count = Taskactivity.objects.filter(due_date__lt=timezone.now()).count()
        context['overdue_tasks_count'] = overdue_tasks_count
        
        return context



from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndeView(LoginRequiredMixin, TemplateView):
    template_name = "indextwo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the logged-in user
        current_user = self.request.user
        
        # Count of complaints for the current user
        context['user_complaint_count'] = complaint_registration.objects.filter(assign_to=current_user).count()
        context['user_task_count'] = Taskactivity.objects.filter(author=current_user).count()
        
        return context


        
        
        
      
        
        
        
       
        
        


class InView(TemplateView):
    template_name = "index3.html"




class EnterLeadView(TemplateView,LoginRequiredMixin):
    template_name = "newlead.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_form'] = CompanyDetailsForm()
        context['contact_form'] = ContactDetailsForm()
        context['business_form'] = BusinessDetailsForm()
        return context

    def post(self, request, *args, **kwargs):
        company_form = CompanyDetailsForm(request.POST)
        contact_form = ContactDetailsForm(request.POST)
        business_form = BusinessDetailsForm(request.POST)
        
        if company_form.is_valid() and contact_form.is_valid() and business_form.is_valid():
            # Save each form individually
            company_instance = company_form.save()
            contact_instance = contact_form.save()
            business_instance = business_form.save(commit=False)  
            business_instance.company = company_instance
            business_instance.contact = contact_instance
            business_instance.save()

            # Create a new Customer instance using the data
            lead_instance = Lead.objects.create(
                company_name=company_instance.company,
                first_name=company_instance.firstname,
                email=contact_instance.email,
                mobile=contact_instance.mobile,
                mobile_country_code=contact_instance.mobile_country_code,
                country=contact_instance.country,
                state=contact_instance.state,
                city=contact_instance.city,
                executive_name=business_instance.executive_name,
                exe_designation=business_instance.exe_designation,
                source=business_instance.source,
                product=business_instance.product,
                requirement=business_instance.requirement,
                notes=business_instance.notes,
                stages=business_instance.stages,
                industry_type=business_instance.industry_type,
                gst=business_instance.gst,
                created_by=request.user 
            )

            return redirect('list')  
        else:
            # Print form errors
            print("Company Form Errors:", company_form.errors)
            print("Contact Form Errors:", contact_form.errors)
            print("Business Form Errors:", business_form.errors)
            return self.render_to_response(self.get_context_data(company_form=company_form, contact_form=contact_form, business_form=business_form))



# class LeadListView(ListView):
#     model = Lead
#     template_name = "leadlist.html"
#     context_object_name = "leads"

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         search_query = self.request.GET.get('q')

#         if search_query:
#             queryset = queryset.filter(
#                 Q(first_name__icontains=search_query) |
#                 Q(mobile__icontains=search_query) |
#                 Q(company_name__icontains=search_query)
#             )

#         return queryset

from django.views.generic import ListView
from django.db.models import Q, Max
from .models import Taskactivity
from .forms import TaskActivityForm
from django.contrib import messages
from django.shortcuts import redirect

class LeadListView(ListView,LoginRequiredMixin):
    model = Lead
    template_name = "leadsone.html"
    context_object_name = "leads"

    def get_queryset(self):
        queryset = super().get_queryset().filter(created_by=self.request.user)
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(mobile__icontains=search_query) |
                Q(company_name__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        leads = context['leads']
        
        # Get the latest task activity for each lead and add it to the context
        for lead in leads:
            lead.latest_task_activity = Taskactivity.objects.filter(related_to=lead).order_by('-date_created').first()
        
        context['task_form'] = TaskActivityForm()
        context['lead_count'] = Lead.objects.filter(created_by=self.request.user).count()
        context['users'] = CustomUser.objects.all()
        
        stages_counts = Lead.objects.filter(created_by=self.request.user).values('stages__name').annotate(count=Count('stages')).order_by('stages__name')
        context['stages_counts'] = stages_counts
        return context
    
    def post(self, request, *args, **kwargs):
        if 'task_title' in request.POST:
            form = TaskActivityForm(request.POST, request.FILES)
            if form.is_valid():
                task_activity = form.save(commit=False)
                task_activity.author = request.user
                task_activity.save()
                messages.success(request, "Task created successfully")
                return redirect('list')  # Redirect to a success page or list view
        return super().get(request, *args, **kwargs)


    
        

   

@login_required
def convert_lead_to_customer(request, lead_id):
    # Retrieve the lead object
    lead = get_object_or_404(Lead, pk=lead_id)

    
    customer = Customer.objects.create(
        author=request.user,
        company_name=lead.company_name,
        first_name=lead.first_name,
        email=lead.email,
        mobile=lead.mobile,
        mobile_country_code=lead.mobile_country_code,
        country=lead.country,
        state=lead.state,
        city=lead.city,
        executive_name=lead.executive_name,
        exe_designation=lead.exe_designation,
        source=lead.source,
        product=lead.product,
        requirement=lead.requirement,
        notes=lead.notes,
        stages=lead.stages,
        industry_type=lead.industry_type,
        gst=lead.gst
    )

    
    lead.delete()

    return redirect('list')



from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Lead, contact_details, bussiness_details, company_details
from .forms import LeadChangeForm

class LeadEditView(UpdateView):
    model = Lead
    form_class = LeadChangeForm
    template_name = "leadedit.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        response = super().form_valid(form)
        lead = form.instance

        # Handle contact_details update
        contacts = contact_details.objects.filter(id=lead.id)
        for contact in contacts:
            contact.mobile=lead.mobil
            contact.mobile_country_code = lead.mobile_country_code
            contact.email = lead.email
            contact.country = lead.country
            contact.state = lead.state
            contact.city = lead.city
            contact.save()

        # Handle bussiness_details update
        business = bussiness_details.objects.filter(id=lead.id)
        for bus in business:
            bus.executive_name = lead.executive_name
            bus.exe_designation = lead.exe_designation
            bus.source = lead.source
            bus.product = lead.product
            bus.requirement = lead.requirement
            bus.notes = lead.notes
            bus.industry_type = lead.industry_type
            bus.gst = lead.gst
            bus.save()

        # Handle company_details update
        companies = company_details.objects.filter(id=lead.id)
        for company in companies:
            company.firstname = lead.first_name
            # Assuming you want to update lastname from some field in Lead, add that field to Lead model if not present
           
            company.save()

        return response














    




# from django.shortcuts import get_object_or_404
# from django.views.generic import DetailView
# from .models import Lead, Employee, TaskActivity,AppointmentActivity

# class LeadDetailView(DetailView):
#     model = Lead
#     template_name = "newleaddetail.html"
#     context_object_name = "lead"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['employees'] = Employee.objects.all()
#         return context

#     def post(self, request, *args, **kwargs):
#         # Handle task form submission
#         if 'task_title' in request.POST:
#             related_to = request.POST.get('related_to')
#             task_title = request.POST.get('task_title')
#             assigned_to_id = request.POST.get('assigned_to')
#             due_date = request.POST.get('due_date')
#             priorty = request.POST.get('priorty')
#             task_description = request.POST.get('task_description')
#             attachment = request.FILES.get('attachment')

#             assigned_to = get_object_or_404(Employee, pk=assigned_to_id)

#             TaskActivity.objects.create(
#                 related_to=related_to,
#                 task_title=task_title,
#                 assigned_to=assigned_to,
#                 due_date=due_date,
#                 priorty=priorty,
#                 task_description=task_description,
#                 attachment=attachment
#             )

#         # Handle appointment form submission
#         elif 'appointment_type' in request.POST:
#             appointment_type = request.POST.get('appointment_type'),
#             related_to = request.POST.get('related_to')
#             description = request.POST.get('description')
#             from_date_time = request.POST.get('from_date_time')
#             to_date_time = request.POST.get('to_date_time')
#             location = request.POST.get('location')
#             assigned_to_id = request.POST.get('assigned_to')
            

#             attendees = get_object_or_404(Employee, pk=assigned_to_id)

#             appointment = AppointmentActivity.objects.create(
#                 appointment_type=appointment_type,
#                 description=description,
#                 from_date_time=from_date_time,
#                 to_date_time=to_date_time,
#                 location=location,
                
#                 attendees=attendees,
#                 related_to=related_to
#             )
            

#         return super().get(request, *args, **kwargs)



class LeadDetailView(DetailView):
    model = Lead
    template_name = "newleaddetail.html"
    context_object_name = "lead"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.all()
        # Add related TaskActivity objects to the context
        context['task_activities'] = Taskactivity.objects.filter(related_to=self.object)
        
        return context

    def post(self, request, *args, **kwargs):
        # Handle task form submission
        if 'task_title' in request.POST:
            related_to_id = request.POST.get('related_to') 
            task_title = request.POST.get('task_title')
            assigned_to_id = request.POST.get('assigned_to')
            due_date = request.POST.get('due_date')
            priorty = request.POST.get('priorty')
            task_description = request.POST.get('task_description')
            attachment = request.FILES.get('attachment')

            related_to = get_object_or_404(Lead, pk=related_to_id)
            assigned_to = get_object_or_404(Employee, pk=assigned_to_id)

            Taskactivity.objects.create(
                related_to=related_to,
                task_title=task_title,
                assigned_to=assigned_to,
                due_date=due_date,
                priorty=priorty,
                task_description=task_description,
                attachment=attachment
            )

        # Handle appointment form submission
        elif 'appointment_type' in request.POST:
            appointment_type = request.POST.get('appointment_type')
            related_to = request.POST.get('related_to')
            description = request.POST.get('description')
            from_date_time = request.POST.get('from_date_time')
            to_date_time = request.POST.get('to_date_time')
            location = request.POST.get('location')
            assigned_to_id = request.POST.get('assigned_to')

            attendees = get_object_or_404(Employee, pk=assigned_to_id)

            AppointmentActivity.objects.create(
                appointment_type=appointment_type,
                description=description,
                from_date_time=from_date_time,
                to_date_time=to_date_time,
                location=location,
                attendees=attendees,
                related_to=related_to
            )

        return super().get(request, *args, **kwargs)






class TaskListView(ListView):
    model = Taskactivity
    template_name = "tlist.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter')
        specific_date = self.request.GET.get('date')
        today = timezone.now().date()
        
        # Filter tasks by the authenticated user
        queryset = queryset.filter(author=self.request.user)

        if filter_type == 'overdue':
            queryset = queryset.filter(due_date__lt=today)
        elif filter_type == 'current':
            queryset = queryset.filter(due_date=today)
        elif filter_type == 'tomorrow':
            tomorrow = today + timezone.timedelta(days=1)
            queryset = queryset.filter(due_date=tomorrow)
        elif specific_date:
            try:
                specific_date = timezone.datetime.strptime(specific_date, '%Y-%m-%d').date()
                queryset = queryset.filter(due_date=specific_date)
            except ValueError:
                queryset = queryset.none()
        
        return queryset


class TaskDetailView(DetailView):
    model=Taskactivity
    template_name="tdetail.html"
    context_object_name="task"    

# def task_delete_view(request,*args,**kargs):
#     id=kargs.get("pk")
#     Taskactivity.objects.get(id=id).delete()
#     messages.success(request,"task removed")
#     return redirect("tasklist")




def task_delete_view(request, *args, **kwargs):
    id = kwargs.get("pk")
    task = Taskactivity.objects.get(id=id)

    # Save the task details in the DeletedTask table
    DeletedTask.objects.create(
        
        date_created=task.date_created,
        task_title=task.task_title,
        due_date=task.due_date,
        priorty=task.priorty,
        task_description=task.task_description,
        attachment=task.attachment,
        assigned_to=task.assigned_to,
        author=task.author,
        related_to=task.related_to
    )

    # Delete the task
    task.delete()

    messages.success(request, "Task removed")
    return redirect("tasklist")

class AppointmentListView(ListView):
    model=AppointmentActivity
    template_name="appointmentlist.html"
    context_object_name="appointments"

class DeletedTaskListView(ListView):
    model=DeletedTask
    template_name="deletedtasklist.html"
    context_object_name="dtasks"    


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Taskactivity

def start_task_view(request, pk):
    task = get_object_or_404(Taskactivity, pk=pk)
    task.status = 'inprogress'
    task.save()
    messages.success(request, "Task marked as in progress")
    return redirect('tasklist')  # Redirect to the task list view

def complete_task_view(request, pk):
    task = get_object_or_404(Taskactivity, pk=pk)
    task.status = 'completed'
    task.save()
    messages.success(request, "Task marked as completed")
    return redirect('tasklist')  # Redirect to the task list view






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from .models import ClockIn

@login_required
def clock_in(request):
    today = now().date()
    user = request.user

    # Check if the user has already clocked in and clocked out today
    clock_in_record = ClockIn.objects.filter(user=user, clock_in_time__date=today).first()
    
    if request.method == 'POST':
        if clock_in_record:
            if clock_in_record.clock_out_time is None:
                # Clock out
                clock_in_record.clock_out_time = now()
                clock_in_record.save()
                messages.success(request, 'You have successfully clocked out.')
                response = {'status': 'clocked_out', 'message': {'tags': 'success', 'text': 'You have successfully clocked out.'}}
            else:
                # Already clocked out
                messages.warning(request, 'You have already clocked out for today.')
                response = {'status': 'already_clocked_out', 'message': {'tags': 'warning', 'text': 'You have already clocked out for today.'}}
        else:
            # Clock in
            ClockIn.objects.create(user=user, clock_in_time=now())
            messages.success(request, 'You have successfully clocked in.')
            response = {'status': 'clocked_in', 'message': {'tags': 'success', 'text': 'You have successfully clocked in.'}}

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response)

        return redirect('index2')  # Redirect back to the same view to refresh the context

    context = {
        'already_clocked_in': bool(clock_in_record) and clock_in_record.clock_out_time is None,
        'already_clocked_out': bool(clock_in_record) and clock_in_record.clock_out_time is not None,
    }
    return render(request, 'index2.html', context)


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ClockIn
from .forms import MonthYearForm
from datetime import datetime, date, timedelta
import calendar

@login_required
def calendar_view(request):
    user = request.user
    today = datetime.today()

    if request.method == 'POST':
        form = MonthYearForm(request.POST)
        if form.is_valid():
            year = int(form.cleaned_data['year'])
            month = int(form.cleaned_data['month'])
    else:
        form = MonthYearForm()
        year = today.year
        month = today.month

    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, calendar.monthrange(year, month)[1])

    clockins = ClockIn.objects.filter(user=user, clock_in_time__date__range=[first_day_of_month, last_day_of_month]).order_by('clock_in_time')

    presence_dict = {}
    for clockin in clockins:
        clock_in_date = clockin.clock_in_time.date()
        presence_dict[clock_in_date] = True

    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(year, month)

    context = {
        'month_days': month_days,
        'presence_dict': presence_dict,
        'current_month': datetime(year, month, 1).strftime('%B %Y'),
        'form': form,
    }

    return render(request, 'calendar1.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import ClockIn
from datetime import datetime, timedelta

def user_presence(request):
    User = get_user_model()
    users = User.objects.all()

    # Get the month and year from the request or default to current month and year
    month = request.GET.get('month', datetime.now().month)
    year = request.GET.get('year', datetime.now().year)

    # Ensure month is within valid range (1 to 12)
    try:
        month = int(month)
        if month < 1 or month > 12:
            raise ValueError("Month must be in the range 1 to 12")
    except ValueError:
        month = datetime.now().month  # Default to current month if invalid

    # Calculate the first and last day of the specified month and year
    first_day = datetime(int(year), month, 1).date()
    next_month = month % 12 + 1
    next_year = int(year) + (1 if next_month == 1 else 0)
    last_day = datetime(next_year, next_month, 1).date() - timedelta(days=1)

    # Generate all dates in the specified month and year
    all_dates = [first_day + timedelta(days=x) for x in range((last_day - first_day).days + 1)]

    # Query clock-in records for the specified month and year
    clock_in_records = ClockIn.objects.filter(
        clock_in_time__year=int(year),
        clock_in_time__month=month
    )

    # Create a dictionary to hold user presence status
    user_presence_status = {}

    for user in users:
        user_presence_status[user] = [False] * len(all_dates)

    for record in clock_in_records:
        index = (record.clock_in_time.date() - first_day).days
        user_presence_status[record.user][index] = True

    context = {
        'user_presence_status': user_presence_status,
        'dates': all_dates,
        'year': year,
        'month': month,
    }

    return render(request, 'user_presence.html', context)


















   
    
























