from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from auth_.models import Profile


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = User.objects.get(id=instance.user.id)
    user.delete()


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
