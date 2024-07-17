from django import forms
from django.contrib.auth.models import Permission
from .models import Role

# class RolePermissionForm(forms.Form):
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Role")
#     permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         label="Permissions"
#     )

class RolePermissionForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Role")
    
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Permissions"
    )

    def __init__(self, *args, **kwargs):
        super(RolePermissionForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].widget.attrs.update({
            'class': 'permissions-checkbox'
        })
        self.permission_groups = {
            'log entry': [1, 2, 3, 4],  # Permission IDs for Group 1
            'auth group ': [5, 6, 7, 8],  # Permission IDs for Group 2
            'auth permission': [9,10,11,12],
              'contenttypes':[13,14,15,16],
                'session':[17,18,19,20],
                  'city':[21,22,23,24], 
                   'company details':[25,26,27,28],
                   'country':[29,30,31,32],
                   'taskactivity':[33,34,35,36],
                   'state':[37,38,39,40],
                   'lead':[41,42,43,44],
                   'contact details':[45,46,47,48],
                   'bussiness details':[49,50,51,52],
                   'appointmentactivity':[53,54,55,56],
                   'customer complaintregistration':[57,58,59,60],
                   'customer':[61,62,63,64],
                   'employee':[65,66,67,68],
                   'tasksettings':[69,70,71,72],
                     # Permission IDs for Group 3
            # Add more groups as needed
        }









