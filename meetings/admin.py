from django.contrib import admin

from .models import Orga, Meeting


class OrgaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Orga, OrgaAdmin)


class MeetingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Meeting, MeetingAdmin)
