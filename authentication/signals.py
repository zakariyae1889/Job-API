from django.db.models.signals import post_delete,post_save
from  django.dispatch import receiver
from .models import Profile
from utils.cache.cache_utils import safe_cache_delete
@receiver([post_delete,post_save],sender=Profile)
def clear_profile_cache(sender,instance,**kwargs):
    safe_cache_delete(f"user_{instance.user.id}_profile")

    safe_cache_delete("all_profiles")

