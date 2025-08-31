from django.db import models
from django.conf import settings
from job.models import Job
from django.core.validators import MaxValueValidator ,MinValueValidator
# Create your models here.

class Review(models.Model):
    jobseeker= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jobseeker.username}->{self.job.title}"