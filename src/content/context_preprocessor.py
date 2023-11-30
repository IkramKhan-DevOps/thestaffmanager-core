from .utils import my_application


def my_site(request):
    return {
        'site': my_application()
    }
