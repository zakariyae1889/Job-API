from django.contrib import admin
from .models import Job,JobHistorySlug
# Register your models here.
admin.site.register(Job)
admin.site.register(JobHistorySlug)