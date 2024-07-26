from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,UpdateView,ListView,DetailView,CreateView
from django.urls import reverse_lazy
from .models import Department
import json
from django.contrib import messages

# Create your views here.


class DepartmentsView(TemplateView):
    template_name="departments.html"

class DepartmentsView(ListView):
    model=Department
    template_name="departmentsone.html"
    context_object_name="departments"




def add_department(request):
    if request.method == "POST":
        stages = request.POST.get('stages')
        if stages:
            stage_names = json.loads(stages)
            for name in stage_names:
                if not Department.objects.filter(name=name).exists():
                    Department.objects.create(name=name)
            messages.success(request, 'Departments added successfully!')
        return redirect('departments-add')  
    return render(request, 'adddepartmentsone.html')
