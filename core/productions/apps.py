from django.apps import AppConfig


class ProductionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.productions'
    label = 'core_productions'

    # def ready(self):
    #     # Importer les signaux
    #     import core.productions.signals