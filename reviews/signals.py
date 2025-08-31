from django.db.models.signals import post_delete,post_save
from .models import Review
from django.dispatch import receiver
from utils.cache.cache_utils import safe_cache_delete

@receiver([post_delete,post_save],sender=Review)
def clear_reviws_cache(instance,*args, **kwargs):

    safe_cache_delete(f"reviews_{instance.job.slug}_slug")
    safe_cache_delete(f"all_reviews")