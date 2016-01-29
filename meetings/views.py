from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Orga


def home(request):
    return render(request, "home.haml", {
        "orga": Orga.get_orga_from_request(request)
    })


class PVPADsViews(object):
    def get_context_data(self, *args, **kwargs):
        context = super(PVPADsViews, self).get_context_data(*args, **kwargs)
        context["orga"] = Orga.get_orga_from_request(self.request)
        return context


class MeetingList(PVPADsViews, TemplateView):
    template_name = "meetings/meeting_list.haml"


