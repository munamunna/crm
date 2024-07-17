from django import forms
from .models import complaint_registration,Customer
import uuid
from accounts.models import CustomUser

class ComplaintRegistrationForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('monitor_issue', 'Monitor Issue'),
        ('printer_not_working', 'Printer Not Working'),
    )

    # PERSON_TYPE_CHOICES = (
    #     ('client', 'Client'),
    #     ('employee', 'Employee'),
    # )

    # person_type = forms.ChoiceField(choices=PERSON_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    requester_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    designation = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=40, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    complaint = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    defult_issues = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-contrl form-control'}))
    assign_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), empty_label="Select a staff member" ,required=False)

    class Meta:
        model = complaint_registration
        fields = ['person_type', 'requester_name', 'designation', 'phone_number', 'email', 'complaint', 'defult_issues','assign_to','status','priority']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assign_to'].label_from_instance = lambda obj: obj.first_name
    
    


class CustomerChangeForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'




class ComplaintChangeForm(forms.ModelForm):
    class Meta:
        model = complaint_registration
        fields = ['assign_to', 'status', 'priority']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['assign_to'].queryset = CustomUser.objects.filter(reportee=user)
            self.fields['assign_to'].label_from_instance = lambda obj: obj.first_name
