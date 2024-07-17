from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm,PasswordResetForm
from django.contrib.auth import authenticate,login,logout
from django.views.generic import ListView,TemplateView,FormView
from .signals import update_user_permissions
from .models import CustomUser

from django.shortcuts import render, redirect


def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully')
            return redirect('register')  # Adjust this to your desired redirect URL
    else:
        form = CustomUserCreationForm()

    return render(request, 'add_user.html', {'form': form})

class UsersView(ListView):
    model=CustomUser
    template_name="users.html"
    context_object_name="users"

# def user_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         # update_user_permissions(CustomUser, user)
#         if user is not None:
#             login(request, user)
#             return redirect('index')  # Adjust this to your desired redirect URL
#         else:
#             messages.error(request, 'Invalid email or password')
#     return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('index')  # Redirect to index for superusers
            else:
                return redirect('index2')  # Redirect to index2 for regular users
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')


def sign_out_view(request,*args,**kargs):
    logout(request)
    return redirect("login")

# class UsersView(TemplateView):
#     template_name="users.html"

class PermissionlView(TemplateView):
    template_name = "permission.html"




class PasswordResetView(FormView):
    model = CustomUser
    template_name = "password-reset.html"
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if password == confirm_password:
                try:
                    usr = CustomUser.objects.get(email=email)
                    usr.set_password(password)
                    usr.save()
                    messages.success(request, "Password changed successfully.")
                    return redirect("login")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Invalid email address.")
                except Exception as e:
                    messages.error(request, "An error occurred. Please try again.")
            else:
                messages.error(request, "Passwords do not match.")

        # If the form is not valid or there is any error, re-render the form with errors
        return render(request, self.template_name, {"form": form})






