from django.db import models,transaction
from django.utils.text import slugify
from django.conf import settings
import uuid

class Companies(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    web = models.URLField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="companies")
    descriptions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old = Companies.objects.only("name","slug").get(pk=self.pk)
                if old.name != self.name:  # الاسم تغيّر
                    # خزّن السجل القديم
                    CompanyHistorySlug.objects.create(Companies=self,old_slug=old)
                    # أنشئ slug جديد بناءً على الاسم الجديد
                    base_slug = slugify(self.name, allow_unicode=True)
                    unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                    self.slug = unique_slug
            else:
                base_slug=slugify(f"{self.name}",allow_unicode=True)
                uinque_slug=f"{base_slug}-{uuid.uuid4().hex[:8]}"
                self.slug=uinque_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CompanyHistorySlug(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name="company_slug_history")
    old_slug = models.SlugField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.company.slug}:{self.old_slug}'
