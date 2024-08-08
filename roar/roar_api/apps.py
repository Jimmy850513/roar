from django.apps import AppConfig


class RoarApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roar_api'

    def ready(self):
        from job import updater
        updater.strat()
        
