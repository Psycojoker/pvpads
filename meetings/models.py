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
            pass

        try:
            return klass.objects.get(default=True)
        except klass.DoesNotExist:
            return None

    def __unicode__(self):
        return self.name


class Meeting(models.Model):
    orga = models.ForeignKey(Orga)

    title = models.CharField(max_length=255, null=True, blank=True, help_text="will be the first non-empty line of the pad content if left empty")
    url = models.URLField()
    meeting_date = models.DateField()

    slug = models.SlugField(null=True, blank=True, help_text="will be deduced from the pad title if left empty")

    content = models.TextField(editable=False, null=True, blank=True)
    html = models.TextField(editable=False, null=True, blank=True)

    last_modification = models.DateTimeField(auto_now=True)
