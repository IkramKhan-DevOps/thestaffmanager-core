from .models import Application


def my_application():
    application = Application.objects.all()
    if application.count() == 0:
        application = Application.objects.create()
    else:
        application = application[0]

    return application
