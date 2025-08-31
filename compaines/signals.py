from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Companies
from utils.cache.cache_utils import safe_cache_delete

@receiver([post_delete,post_save],sender=Companies)
def clear_companies_cache(sender,instance,*args, **kwargs):
    safe_cache_delete("all_compainces")
    safe_cache_delete(f"slug_{instance.slug}_compaines")