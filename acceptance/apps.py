from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class AcceptanceConfig(AppConfig):
    name = 'acceptance'

    def ready(self):
        import acceptance.signals
