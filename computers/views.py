from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from computers.models import Computer,VideoCard,Motherboard,Processor,PowerUnit


class ShowComputersView(TemplateView):
    template_name = "computers/show_computers.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
       context = super().get_context_data(**kwargs)
       context['computers'] = Computer.objects.all()
       context['VideoCard'] = VideoCard.objects.all()
       context['Motherboard'] = Motherboard.objects.all()
       context['Processor'] = Processor.objects.all()
       context['PowerUnit'] = PowerUnit.objects.all()

       return context
