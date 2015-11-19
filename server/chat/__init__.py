default_app_config = 'chat.AppConfig'

from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import (
    ugettext_lazy as _,
)


class AppConfig(DjangoAppConfig):
    name = 'chat'
    verbose_name = _("Alumni")

    def ready(self):
        import tasks        # NOQA
