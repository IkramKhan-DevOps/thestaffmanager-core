from django.apps import AppConfig
from core.settings import DEFAULT_AUTO_FIELD


class ContentConfig(AppConfig):
    name = 'src.content'
    default_auto_field = DEFAULT_AUTO_FIELD

    def ready(self):
        from src.content import signals
