from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^meeting/$', views.MeetingList.as_view(), name='meeting_list'),
]
