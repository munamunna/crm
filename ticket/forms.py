from django import forms
from .models import Ticketss
from customer.models import Customer
from accounts.models import CustomUser

class TicketssForm(forms.ModelForm):
    requester_name = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a requester",
          # Customize the label as needed
    )
    assign_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        empty_label="Select a staff member",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
    max_length=250, 
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
)

    class Meta:
        model = Ticketss
        fields = ['requester_name', 'priority', 'status','description','assign_to']
        widgets = {
            'assign_to': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assign_to'].label_from_instance = lambda obj: obj.first_name
   
    