import os

from urllib2 import urlopen

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

    format = models.CharField(max_length=255, choices=FORMATS)

    slug = models.SlugField(null=True, blank=True, help_text="will be deduced from the pad title if left empty")

    content = models.TextField(editable=False, null=True, blank=True)
    html = models.TextField(editable=False, null=True, blank=True)

    last_modification = models.DateTimeField(auto_now=True)

    def update_and_render_content(self):
        try:
            self.content = urlopen(os.path.join(self.url, "export/txt")).read()
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stdout)
            print("Exception: %s" % e)
            print("Error: get fetch the content of %s" % self.url)
            return

    def save(self, *args, **kwargs):
        if not self.content:
            self.update_and_render_content()

        if not self.title:
            maybe_title = filter(None, map(lambda x: x.strip(), self.content.split("\n")))
            if maybe_title:
                self.title = maybe_title[0]

        return super(Meeting, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s - %s" % (self.title, self.url)

    class Meta:
        ordering = ["-date"]
        unique_together = (('url', 'orga'))
