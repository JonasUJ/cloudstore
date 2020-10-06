from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, signals
from django.dispatch import receiver

from rest_framework.authtoken.models import Token  # pylint: disable=import-error

from ..api.models import Folder  # noqa pylint: disable=import-error


class CloudstoreUser(AbstractUser):
    base_folder = models.ForeignKey(Folder, default=None, null=True, on_delete=models.DO_NOTHING)


class UserSettings(models.Model):
    user = models.OneToOneField(CloudstoreUser, on_delete=models.CASCADE, related_name='settings')
    theme = models.CharField(max_length=8, default='dark')
    view = models.CharField(max_length=8, default='tiles')
    view_img = models.BooleanField(default=True)
    show_ext = models.BooleanField(default=False)


class UserQuota(models.Model):
    user = models.OneToOneField(CloudstoreUser, on_delete=models.CASCADE, related_name='quota')
    allowed = models.BigIntegerField(default=0)
    used = models.BigIntegerField(default=0)

    def _change(self, amount):
        self.used = F('used') + amount
        self.save()

    def use(self, amount):
        self._change(amount)

    def free(self, amount):
        self._change(-amount)

    def __str__(self):
        return f'{self.user}\'s quota ({self.used} / {self.allowed})'


@receiver(signals.post_save, sender=CloudstoreUser)
def user_post_save_receiver(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    if created:
        instance.base_folder = Folder.objects.create(
            owner=instance, name=f'base_folder_{instance.pk}', folder=None
        )
        Token.objects.create(user=instance)
        UserSettings.objects.create(user=instance)
        UserQuota.objects.create(user=instance)
        instance.save()
