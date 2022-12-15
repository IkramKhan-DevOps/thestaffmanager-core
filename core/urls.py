from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from . import settings
from .settings import MEDIA_ROOT, STATIC_ROOT
from django.views.static import serve


def handler404(request, *args, **kwargs):
    return render(request, "404.html")


def handler500(request, *args, **kwargs):
    return render(request, "500.html")


handler404 = handler404
handler500 = handler500

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    # path('', include('src.website.urls', namespace="website")),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('a/', include('src.administration.admins.urls', namespace='admins')),
    path('c/', include('src.administration.employees.urls', namespace='employees')),
]

urlpatterns += [
    path('accounts/', include('allauth.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
