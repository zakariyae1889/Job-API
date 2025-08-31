from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Application
from utils.cache.cache_utils import safe_cache_delete
@receiver([post_save, post_delete], sender=Application)
def signals_receiver(sender,instance, **kwargs):
    safe_cache_delete("all_application")
    safe_cache_delete(f"slug_{instance.slug}_application")