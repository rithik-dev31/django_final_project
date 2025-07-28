# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Section, Community

@receiver(post_save, sender=Section)
def create_community_for_section(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'community'):
        Community.objects.get_or_create(section=instance)