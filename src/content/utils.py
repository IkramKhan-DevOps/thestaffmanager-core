from .models import Application


def my_application():
    obj, created = Application.objects.get_or_create()
    return obj
