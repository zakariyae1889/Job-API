from django.db import models,transaction
from django.utils.text import slugify
import uuid
# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=100000, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:  # إذا كان الكائن موجود مسبقًا
                old = Categories.objects.only("name", "slug").get(pk=self.pk)
                if old.name != self.name:  # الاسم تغيّر
                    # خزّن السجل القديم
                    CategoriesHistorySlug.objects.create(category=self, old_slug=old.slug)
                    # أنشئ slug جديد بناءً على الاسم الجديد
                    base_slug = slugify(self.name, allow_unicode=True)
                    unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                    self.slug = unique_slug
            else:
                # إنشاء لأول مرة
                base_slug = slugify(self.name, allow_unicode=True)
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CategoriesHistorySlug(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="slug_history")
    old_slug = models.SlugField(blank=True, null=True, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.slug}-{self.old_slug}"