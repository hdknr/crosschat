from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SocketUser(models.Model):
    user = models.OneToOneField(User)
    key = models.CharField(_('User Key'), max_length=50)

    class Meta:
        verbose_name = _('Socket User')
        verbose_name_plural = _('Socket User')

    def __unicode__(self):
        return self.user and self.user.username


class Topic(models.Model):
    name = models.CharField(_('Topic Name'), max_length=50)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topic')

    def __unicode__(self):
        return self.name


class TopicUser(models.Model):
    topic = models.ForeignKey(Topic)
    user = models.ForeignKey(SocketUser)

    class Meta:
        verbose_name = _('Topic User')
        verbose_name_plural = _('Topic User')


from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import uuid


@receiver(user_logged_in)
def on_user_login(sender, user, request, **kwargs):
    res = SocketUser.objects.filter(user=user).update(key=uuid.uuid1().hex)
    if res < 1:
        SocketUser.objects.create(user=user, key=uuid.uuid1().hex)
