from django.contrib import admin
from .models import Project, ProjectFile, Supervisor
# Register your models here.
admin.site.register(Project)
admin.site.register(Supervisor)
admin.site.register(ProjectFile)