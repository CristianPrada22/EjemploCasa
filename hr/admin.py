from django.contrib import admin
from .models import Advertisement, Interview, JobDescription, Recruitment, Area
# Register your models here.

admin.site.register(Interview)
admin.site.register(Area)
admin.site.register(JobDescription)
admin.site.register(Recruitment)
admin.site.register(Advertisement)
