import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from accounts.models import Profile


@receiver(pre_delete, sender=Profile)
def delete_avatar(sender, instance, **kwargs):
    if os.path.isfile(instance.avatar.path):
        os.remove(instance.avatar.path)
