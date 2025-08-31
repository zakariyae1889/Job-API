from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Categories
from utils.cache.cache_utils import safe_cache_delete

@receiver([post_save,post_delete],sender=Categories)
def clear_categories_cache(sender,instance,*args, **kwargs):
    
    safe_cache_delete(f"categories_{instance.slug}")
    safe_cache_delete("all_categories")


    
   