from django.apps import AppConfig


class NopgonAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nopgon_auth'

    def ready(self):
        import nopgon_auth.signals
