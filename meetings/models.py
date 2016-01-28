from __future__ import unicode_literals

from django.db import models


class Orga(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    home_html = models.TextField()
    page_html = models.TextField()
    css = models.TextField()

    default = models.BooleanField(default=False)


class Meeting(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField()
    meeting_date_time = models.DateTimeField()

    slug = models.SlugField(null=True, blank=True)

    content = models.TextField(editable=False, null=True, blank=True)
    html = models.TextField(editable=False, null=True, blank=True)

    last_modification = models.DateTimeField(auto_now=True)
