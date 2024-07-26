from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,UpdateView,ListView,DetailView,CreateView
from django.urls import reverse_lazy
from .models import Role
from accounts.models import CustomUser
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Permission
from django.contrib import messages
from .models import Role
from .forms import RolePermissionForm
from django.db.models import Count

# Create your views here.
# class GeneralView(TemplateView):
#     template_name="generalsettings.html"

# class RolesView(TemplateView):
#     template_name="roles.html"






# def add_role(request):
#     if request.method == "POST":
#         stages = request.POST.get('stages')
#         if stages:
#             stage_names = json.loads(stages)
#             for name in stage_names:
#                 if not Role.objects.filter(name=name).exists():
#                     Role.objects.create(name=name)
#         return redirect('roles-add')  
#     return render(request, 'addroles.html')

def add_role(request):
    if request.method == "POST":
        stages = request.POST.get('stages')
        if stages:
            stage_names = json.loads(stages)
            for name in stage_names:
                if not Role.objects.filter(name=name).exists():
                    Role.objects.create(name=name)
            messages.success(request, 'Roles added successfully!')
        return redirect('roles-add')  
    return render(request, 'addrolesone.html')








def assign_permissions(request):
    if request.method == "POST":
        form = RolePermissionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            permissions = form.cleaned_data['permissions']
            role.permissions.set(permissions)
            role.save()
            messages.success(request, "Permissions successfully assigned to the role.")
            return redirect('roles')
    else:
        form = RolePermissionForm()
    return render(request, 'assign_permissions.html', {'form': form})


class RolesView(ListView):
    model = Role
    template_name = "rolesone.html"
    context_object_name = "roles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        roles_with_counts = Role.objects.annotate(user_count=Count('customuser'))
        context['roles_with_counts'] = roles_with_counts
        return context

# class RoleDetailView(DetailView):
#     model=Role
#     template_name="role-detail.html"
#     context_object_name="role"

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .forms import RolePermissionForm

class RoleDetailView(DetailView):
    model = Role
    template_name = "rele_de.html"
    context_object_name = "role"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_permission_form'] = RolePermissionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RolePermissionForm(request.POST)
        if form.is_valid():
            # Process the form data here
            role = form.cleaned_data['role']
            permissions = form.cleaned_data['permissions']
            role.permissions.set(permissions)
            role.save()
            messages.success(request, "Permissions successfully assigned to the role.")
            return redirect('roles')
            
        else:
            return self.render_to_response(self.get_context_data(role_permission_form=form))