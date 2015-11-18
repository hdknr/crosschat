from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from cross.models import Topic


class Room(Topic):
    name = models.CharField(
        _('Room Name'), max_length=50, unique=True)
    description = models.TextField(
        _('Room Description'), null=True, default=None, blank=True)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Room')
        permissions = (
            ('join_anyroom',  'Join Any Room', ),
        )

    def is_authorized(self, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user and user.has_perm('chat.join_anyroom'):
            return True
        return self.topicuser_set.filter(user__user=user).exists()
