from django.db import models
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
