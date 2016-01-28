from django.shortcuts import render
from django.views.generic import ListView

from .models import Orga


def home(request):
    return render(request, "home.haml", {
        "orga": Orga.get_orga_from_request(request)
    })


class MeetingList(ListView):
    template_name = "meetings/meeting_list.haml"

    def get_queryset(self):
        self.orga = Orga.get_orga_from_request(self.request)
        return self.orga.meeting_set.all()

    def get_context_data(self):
        context = super(MeetingList, self).get_context_data()
        context["orga"] = self.orga
        return context
