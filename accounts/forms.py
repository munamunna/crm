from django import forms
from .models import CustomUser, UserType

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'mobile', 'gender', 'user_type', 'date_of_birth', 'country', 'state', 'city', 'department', 'occupation', 'role', 'pincode', 'address', 'reportee','profile_pic']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class PasswordResetForm(forms.Form):
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="new password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    confirm_password=forms.CharField(label="confirm password",widget=forms.PasswordInput(attrs={"class":"form-control"}))