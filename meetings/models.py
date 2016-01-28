
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

    slug = models.SlugField(null=True, blank=True, help_text="will be deduced from the pad title if left empty")

    content = models.TextField(editable=False, null=True, blank=True)
    html = models.TextField(editable=False, null=True, blank=True)

    last_modification = models.DateTimeField(auto_now=True)
