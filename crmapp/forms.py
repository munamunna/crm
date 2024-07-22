from django import forms
from .models import company_details, contact_details, bussiness_details,Taskactivity
from .models import Country, State, City,Designation,Source ,IndustryType

from .models import Lead
from employee.models import Employee
from leadstage.models import LeadStage
from accounts.models import CustomUser


   

class CompanyDetailsForm(forms.ModelForm):

    class Meta:
        model = company_details
        fields = ['company', 'status', 'firstname', 'lastname']
        
       
        TITLE_CHOICES = [
            ('', 'Mr'),
            ('Mr', 'Mr'),
            ('Mrs', 'Mrs'),
            ('Ms', 'Ms'),
        ]
        
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=TITLE_CHOICES),
            'firstname': forms.TextInput(attrs={'class': 'form-control','placeholder': ' First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control','placeholder': ' Last Name'}),
        }






class ContactDetailsForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_country_code = forms.ChoiceField(choices=[('+91', '+91'), ('+971', '+971')], widget=forms.Select(attrs={'class': 'form-control'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Select Country', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label='Select State', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label='Select City', required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = contact_details
        fields = [ 'email','mobile','mobile_country_code','country','state','city']


   







class TaskActivityForm(forms.ModelForm):
    task_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=True)
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), empty_label='Select employee', widget=forms.Select(attrs={'class': 'form-select'}))
    related_to = forms.ModelChoiceField(queryset=Lead.objects.all(), empty_label='Select ', widget=forms.Select(attrs={'class': 'form-select'}))
    due_date = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=True)  # DateInput widget for date selection
    priorty = forms.ChoiceField(choices=Taskactivity.PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    task_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Taskactivity
        fields = [ 'task_title', 'assigned_to', 'related_to', 'due_date', 'priorty', 'task_description' ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].label_from_instance = lambda obj: obj.first_name

class BusinessDetailsForm(forms.ModelForm):
    
    executive_name = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), 
        empty_label='Select exe', 
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    exe_designation = forms.ModelChoiceField(queryset=Designation.objects.all(), empty_label='Select des', widget=forms.Select(attrs={'class': 'form-select'}),required=False)
    source = forms.ModelChoiceField(queryset=Source.objects.all(), empty_label='Select src', widget=forms.Select(attrs={'class': 'form-select'}),required=False)
    
    
    product = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    requirement = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,  
                'cols': 40  
            }
        ),
        required=False
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,  
                'cols': 40  
            }
        ),
        required=False
    )
    stages = forms.ModelChoiceField(queryset=LeadStage.objects.all(), empty_label='Select stage', widget=forms.Select(attrs={'class': 'form-select'}),required=False)
    industry_type = forms.ModelChoiceField(queryset=IndustryType.objects.all(), empty_label='Select Industry_type', widget=forms.Select(attrs={'class': 'form-select'}),required=False)
      
    gst = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    
    

    class Meta:
        model = bussiness_details
        fields = [ 'executive_name', 'exe_designation', 'source', 'product', 'requirement', 'notes','stages','industry_type','gst' ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the label for executive_name field to show the first_name
        self.fields['executive_name'].label_from_instance = lambda obj: obj.first_name
        # Set default initial value for stages field
        try:
            new_stage = LeadStage.objects.get(name="new")
            self.fields['stages'].initial = new_stage
        except LeadStage.DoesNotExist:
            pass


class LeadChangeForm(forms.ModelForm):
    contact_details = ContactDetailsForm()
    company_details = CompanyDetailsForm()
    business_details = BusinessDetailsForm()
    executive_name = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), 
        empty_label='Select exe', 
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    requirement = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,  
                'cols': 40  
            }
        ),
        required=False
    )
    exe_designation = forms.ModelChoiceField(queryset=Designation.objects.all(), empty_label='Select des', widget=forms.Select(attrs={'class': 'form-select'}),required=False)
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,  
                'cols': 40  
            }
        ),
        required=False
    )
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Select Country', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label='Select State', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label='Select City', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    stages = forms.ModelChoiceField(queryset=LeadStage.objects.all(), empty_label='Select stage', widget=forms.Select(attrs={'class': 'form-select'}),required=False)
    industry_type = forms.ModelChoiceField(queryset=IndustryType.objects.all(), empty_label='Select Industry_type', widget=forms.Select(attrs={'class': 'form-select'}),required=False)
    source= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    product= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    company_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    email= forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),required=False)
    mobile= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    mobile_country_code= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    class Meta:
        model = Lead
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executive_name'].label_from_instance = lambda obj: obj.first_name

   
from .models import ClockIn

class ClockInForm(forms.ModelForm):
    class Meta:
        model = ClockIn
        fields = "__all__"

# forms.py
from django import forms
import datetime

class MonthYearForm(forms.Form):
    current_year = datetime.datetime.now().year
    YEAR_CHOICES = [(r, r) for r in range(2000, current_year + 1)]
    MONTH_CHOICES = [(i, datetime.date(1900, i, 1).strftime('%B')) for i in range(1, 13)]

    year = forms.ChoiceField(choices=YEAR_CHOICES, label="Year", initial=current_year, widget=forms.Select(attrs={'class': 'form-control'}))
    month = forms.ChoiceField(choices=MONTH_CHOICES, label="Month", initial=datetime.datetime.now().month, widget=forms.Select(attrs={'class': 'form-control'}))


