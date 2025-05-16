from django.apps import AppConfig


class UserProfileApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile_api_app'

    def ready(self):
        import user_profile_api_app.signals
