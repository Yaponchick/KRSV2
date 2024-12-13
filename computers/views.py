from typing import Any
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import json
from computers.models import Computer, VideoCard, Motherboard, Processor, PowerUnit

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

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                "username": user.username,
                "user_id": user.id,
                "is_authenticated": True
            })
        else:
            return JsonResponse({"error": "Неверные данные авторизации"}, status=400)
    return JsonResponse({"error": "Метод не поддерживается"}, status=405)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Вы успешно вышли"}, status=200)
