from __future__ import unicode_literals

from django.db import models


class Orga(models.Model):
    name = models.CharField(max_length=255)
    domain_name = models.CharField(max_length=255, unique=True)

    default = models.BooleanField(default=False)

    @classmethod
    def get_orga_from_request(klass, request):
        host = request.META["HTTP_HOST"]

        try:
            return klass.objects.get(domain_name=host)
        except klass.DoesNotExist:
            return None


class Meeting(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField()
    meeting_date_time = models.DateTimeField()

    slug = models.SlugField(null=True, blank=True)

    content = models.TextField(editable=False, null=True, blank=True)
    html = models.TextField(editable=False, null=True, blank=True)

    last_modification = models.DateTimeField(auto_now=True)
