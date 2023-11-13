from .models import Application


def my_application():
    created, obj = Application.objects.get_or_create()
    return obj
