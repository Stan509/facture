from django.apps import AppConfig
from AppCaisse import signals

class AppcaisseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "AppCaisse"
    
    
    def ready(self):
        import AppCaisse.signals

