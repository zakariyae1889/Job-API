from django.db import models
from django.conf import settings
from job.models import Job
# Create your models here.

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.title}->{self.user.username}"