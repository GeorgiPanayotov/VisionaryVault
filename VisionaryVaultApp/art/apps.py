from django.apps import AppConfig


class ArtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'VisionaryVaultApp.art'

    def ready(self):
        import VisionaryVaultApp.art.signals

