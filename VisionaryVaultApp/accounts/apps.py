from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'VisionaryVaultApp.accounts'

    def ready(self):
        import VisionaryVaultApp.accounts.signals

