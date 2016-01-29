import sys
import traceback

from django.core.management.base import BaseCommand

from meetings.models import Meeting


class Command(BaseCommand):
    def handle(self, *args, **options):
        for pad in Meeting.objects.all():
            print "[%s]" % pad
            try:
                pad.update_content()
                pad.render_content()
                pad.save()
            except Exception:
                traceback.print_exc(file=sys.stdout)
                print "^ on %s" % pad
