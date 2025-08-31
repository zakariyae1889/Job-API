from django.apps import AppConfig


class CompainesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compaines'

    def ready(self):
        import compaines.signals
