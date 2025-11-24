from django.apps import AppConfig

class ProductoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'producto'

    def ready(self):
        import producto.signals
