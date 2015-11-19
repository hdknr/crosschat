from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models
from cross import config

cross_config = config.load()


@receiver(post_save, sender=models.Announce)
def on_announce(sender=None, instance=None, created=None,
                raw=None, using=None, update_fields=None, **kwargs):
    transport = cross_config.default_transport
    publishers = transport.publishers
    if not created or len(publishers) < 1:
        return

    publisher = publishers[0]

    for _ in publishers:
        if _.options.key:
            publisher = _

    publisher.publish(
        instance.room.uri,
        {"nick": "supervisor", "message": instance.message})
