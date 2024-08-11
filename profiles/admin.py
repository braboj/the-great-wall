from django.contrib import admin

# Register your models here.
from .models import WallProfile, WallSection, Team, WorkLog

admin.site.register(WallProfile)
admin.site.register(WallSection)
admin.site.register(Team)
admin.site.register(WorkLog)
