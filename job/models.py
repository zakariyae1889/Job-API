from django.db import models,transaction
from django.utils.text import slugify
from django.conf import settings
from categories.models import Categories
from compaines.models import Companies
import uuid
# Create your models here.

class TypeJob(models.TextChoices):
    FULL_TIME = "full_time", "Full Time"
    PART_TIME = "part_time", "Part Time"
    FREELANCE = "freelance", "Freelance"
    INTERNSHIP = "internship", "Internship"
    REMOTE = "remote", "Remote"


class Job(models.Model):
    
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="jobs")
    experience = models.CharField(max_length=255, default="1")
    location = models.CharField(max_length=255)
    vacancy = models.PositiveIntegerField(default=0)
    job_nature = models.CharField(max_length=255, choices=TypeJob.choices, default="freelance")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(max_length=100000, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name="jobs")
    posted_date = models.DateTimeField(auto_now_add=True)
    application_date = models.DateTimeField()
   
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)

    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old=Job.objects.only("title","slug").get(pk=self.pk)
                if old.title != self.title:
                    JobHistorySlug.objects.create(job=self, old_slug=old.slug)
                    base_slug = slugify(self.title, allow_unicode=True)
                    unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                    self.slug = unique_slug
            else:
                base_slug = slugify(self.title, allow_unicode=True)
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                self.slug = unique_slug
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title


class JobHistorySlug(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_slug_history")
    old_slug = models.SlugField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job.slug}:{self.old_slug}'

