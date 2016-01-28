from django.shortcuts import render

from .models import Orga


def home(request):
    return render(request, "home.haml", {
        "orga": Orga.get_orga_from_request(request)
    })
