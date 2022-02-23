import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

# from .enums import SetupStatus
from .models import Project

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Project)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Project {instance.name} was created")
        instance.setup_task()
    # else:
    #     if instance.task is not None:
    #         instance.task.enabled = instance.status == SetupStatus.active
    #         instance.task.save()
