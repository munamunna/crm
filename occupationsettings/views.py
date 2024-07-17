from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,UpdateView,ListView,DetailView,CreateView
from django.urls import reverse_lazy
from .models import Occupation
import json
from django.contrib import messages

# Create your views here.
# class GeneralView(TemplateView):
#     template_name="generalsettings.html"

class OccupationView(TemplateView):
    template_name="occupations.html"






def add_occupation(request):
    if request.method == "POST":
        stages = request.POST.get('stages')
        if stages:
            stage_names = json.loads(stages)
            for name in stage_names:
                if not Occupation.objects.filter(name=name).exists():
                    Occupation.objects.create(name=name)
            messages.success(request, 'Occupation added successfully!')
        return redirect('occupation-add')  
    return render(request, 'addoccupation.html')


class OccupationView(ListView):
    model = Occupation
    template_name = "occupations.html"
    context_object_name = "occupations"