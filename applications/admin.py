from django.contrib import admin
from .models import Application, ApplicationSlugHistory


admin.site.register(Application)
admin.site.register(ApplicationSlugHistory)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job_title", "jobseeker")  # اعرض id + عنوان الوظيفة + المستخدم

    def job_title(self, obj):
        return obj.job.title  # جلب العنوان من علاقة Job
    job_title.admin_order_field = "job"   # يخلي العمود يقبل الترتيب
    job_title.short_description = "Job Title"  # العنوان اللي يظهر في الجدول

class ApplicationSlugHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "old_slug", "new_slug", "changed_at")
