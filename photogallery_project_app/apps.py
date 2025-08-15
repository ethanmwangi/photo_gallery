from django.apps import AppConfig

class PhotogalleryProjectAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photogallery_project_app'

    def ready(self):
        import photogallery_project_app.signals
