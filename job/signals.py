from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Job
from utils.cache.cache_utils import safe_cache_delete
@receiver([post_save, post_delete], sender=Job)
def signals_receiver(sender,instance, **kwargs):
    safe_cache_delete("all_job")
    safe_cache_delete(f"slug_{instance.slug}_job")
