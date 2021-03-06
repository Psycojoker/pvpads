import os
import sys
import bleach

from urllib2 import urlopen

from django.db import models

from .format import FORMATS, FORMATTERS, ALLOWED_TAGS


class Orga(models.Model):
    name = models.CharField(max_length=255)
    domain_name = models.CharField(max_length=255, unique=True)

    default = models.BooleanField(default=False, help_text="if the current hostname doesn't match any organisation, this will be the used organisation")

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

    def save(self, *args, **kwargs):
        # ensure that we only have one default orga
        if self.default:
            self.__class__.objects.filter(default=True).exclude(id=self.id).update(default=False)

        return super(Orga, self).save(*args, **kwargs)


class Meeting(models.Model):
    orga = models.ForeignKey(Orga)

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
        unique_together = (('url', 'orga'))
