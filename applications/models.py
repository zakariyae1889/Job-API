from django.db import models, transaction
from django.conf import settings
from django.utils.text import slugify
import uuid

class Application(models.Model):
    job = models.ForeignKey("job.Job", on_delete=models.CASCADE, related_name="applications")
    jobseeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to="applications/", blank=True, null=True)
    status = models.CharField(max_length=20, default="pending")
    slug = models.SlugField(blank=True, null=True, unique=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old= Application.objects.only("job","slug").get(pk=self.pk)
                if old.job.title!=self.job.title:
                    ApplicationSlugHistory.objects.create(application=self, old_slug=old.slug)
                    base_slug = slugify(f"{self.job.title}-{self.jobseeker.username}", allow_unicode=True)
                    unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                    self.slug = unique_slug
            else:
                base_slug = slugify(f"{self.job.title}-{self.jobseeker.username}", allow_unicode=True)
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jobseeker.username}->{self.job.title}"

class ApplicationSlugHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="application_slug_history")
    old_slug = models.SlugField()
    create_at = models.DateTimeField(auto_now_add=True)
