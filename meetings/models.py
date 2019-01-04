import os
import sys
import bleach

from urllib.request import urlopen

from django.db import models

from .format import FORMATS, FORMATTERS, ALLOWED_TAGS


class Meeting(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, help_text="will be the first non-empty line of the pad content if left empty")
    url = models.URLField()
    date = models.DateField()

    format = models.CharField(max_length=255, choices=FORMATS, default="etherpad")

    slug = models.SlugField(null=True, blank=True, help_text="will be deduced from the pad title if left empty")

    content = models.TextField(editable=False, null=True, blank=True)
    html = models.TextField(editable=False, null=True, blank=True)

    last_modification = models.DateTimeField(auto_now=True)

    def update_content(self):
        try:
            self.content = urlopen(os.path.join(self.url, "export/txt")).read()
        except Exception as e:
            try:
                pad_name = self.url.split("/")[-1]
                pad_prefix = "/".join(self.url.split("/")[:-1])
                self.content = urlopen("%s/ep/pad/export/%s/latest?format=txt" % (pad_prefix, pad_name)).read().decode("Utf-8")
            except Exception as e:
                import traceback
                traceback.print_exc(file=sys.stdout)
                print("Exception: %s" % e)
                print("Error: can't fetch the content of %s" % self.url)
                return

    def render_content(self):
        try:
            self.html = bleach.clean(FORMATTERS[self.format][1](self), tags=ALLOWED_TAGS)
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stdout)
            print("Exception: %s" % e)
            print("Error: can't render the content of %s" % self.url)
            return

    def save(self, *args, **kwargs):
        if not self.content:
            self.update_content()
            self.render_content()

        if not self.title:
            maybe_title = filter(None, map(lambda x: x.strip(), self.content.split("\n")))
            if maybe_title:
                self.title = maybe_title[0]

        if not self.slug:
            self.slug = filter(None, self.url.split("/"))[-1]

        if self.id:
            in_db = Meeting.objects.get(id=self.id)

            if in_db.format != self.format:
                self.render_content()

        return super(Meeting, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s - %s" % (self.title, self.url)

    class Meta:
        ordering = ["-date"]
