from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import Orga, Meeting


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


class MeetingDetail(PVPADsViews, DetailView):
    template_name = "meetings/meeting_detail.haml"
    model = Meeting
