from django.apps import AppConfig


class BasefuncConfig(AppConfig):
    verbose_name = 'Main functionality'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basefunc'
