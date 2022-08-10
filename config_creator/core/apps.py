from django.apps import AppConfig
from wordsegment import load


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        load()
