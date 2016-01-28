from django.shortcuts import render

from .models import Orga


def home(request):
    orga = Orga.get_orga_from_request(request)
    return render(request, "home.haml", {
        "orga": orga
    })
