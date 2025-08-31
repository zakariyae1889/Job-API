from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Favorite
from utils.cache.cache_utils import safe_cache_delete
@receiver([post_save, post_delete], sender=Favorite)
def signals_receiver(sender,instance, **kwargs):
    safe_cache_delete("all_favorite")
    safe_cache_delete(f"favorite_{instance.job.slug}_slug")