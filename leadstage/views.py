from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,UpdateView,ListView,DetailView,CreateView
from django.urls import reverse_lazy
from .models import LeadStage
import json
from django.contrib import messages

# Create your views here.
class GeneralView(TemplateView):
    template_name="general.html"

# class LeadstagesView(TemplateView):
#     template_name="leadstages.html"

class LeadstagesView(ListView):
    model=LeadStage
    template_name="leadstagesone.html"
    context_object_name="leadstages"




def add_stage(request):
    if request.method == "POST":
        stages = request.POST.get('stages')
        if stages:
            stage_names = json.loads(stages)
            for name in stage_names:
                if not LeadStage.objects.filter(name=name).exists():
                    LeadStage.objects.create(name=name)
            messages.success(request, 'stage added successfully!')
        return redirect('leadstages-add')  
    return render(request, 'addleadstageone.html')
