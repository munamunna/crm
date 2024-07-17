from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,UpdateView,ListView,DetailView,CreateView
from django.urls import reverse_lazy
from .models import Stage
import json

# Create your views here.
class GeneralView(TemplateView):
    template_name="generalsettings.html"

class TaskstagesView(TemplateView):
    template_name="taskstages.html"






def add_stage(request):
    if request.method == "POST":
        stages = request.POST.get('stages')
        if stages:
            stage_names = json.loads(stages)
            for name in stage_names:
                if not Stage.objects.filter(name=name).exists():
                    Stage.objects.create(name=name)
        return redirect('taskstages-add')  
    return render(request, 'addtaskstage.html')
