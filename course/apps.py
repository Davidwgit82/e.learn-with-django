from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CourseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'course'

    def ready(self):
        from django.contrib.auth import get_user_model
        import os

        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'leasi-ad')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'leasi@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'E.web.py12')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print(f"Superuser {username} créé avec succès !")
