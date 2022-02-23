from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from auth_.models import Profile


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs) -> None:
    user = User.objects.get(id=instance.user.id)
    user.delete()


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs) -> None:
    if created:
        Profile.objects.create(user=instance)
