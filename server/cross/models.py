from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SocketUser(models.Model):
    user = models.OneToOneField(User)
    key = models.CharField(_('User Key'), max_length=50)
    role = models.CharField(_('Role'), max_length=20, default='frontend')
    is_token = models.BooleanField(_('Key Is Token'), default=False)

    class Meta:
        verbose_name = _('Socket User')
        verbose_name_plural = _('Socket User')

    def __unicode__(self):
        return self.user and self.user.username

    def authinfo(self):
        return {
            'username': self.user.username,
            'role': self.role,
            'secret': self.key}


class Topic(models.Model):
    uri = models.CharField(_('Topic URI'), max_length=50)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topic')

    def __unicode__(self):
        return self.uri

    @property
    def instance(self):
        def _cache():
            self._instance = None
            for i in self._meta.related_objects:
                if not issubclass(i.related_model, self._meta.model):
                    continue
                self._instance = i.related_model.objects.filter(
                    **{i.field_name: self.id}).first()
                if self._instance:
                    break
            self._instance = self._instance or self
            return self._instance

        return getattr(self, '_instance', _cache())

    def is_authorized(self, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user and user.is_staff:
            return True
        return self.topicuser_set.filter(user__user=user).exists()


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
