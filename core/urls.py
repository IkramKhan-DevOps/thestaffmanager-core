import notifications
from django.contrib import admin
from django.shortcuts import render, redirect
from django.views.static import serve
from django.urls import path, include, re_path

from .settings import MEDIA_ROOT, STATIC_ROOT, ENVIRONMENT

""" __ ERROR HANDLERS AND VIEWS __ """


def handler404(request, *args, **kwargs):
    return render(request, "404.html")


def handler500(request, *args, **kwargs):
    return render(request, "500.html")


def home(request, *args, **kwargs):
    return redirect('accounts:login')


handler404 = handler404
handler500 = handler500

""" __ URLS __ """

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', home, name='home'),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('a/', include('src.administration.admins.urls', namespace='admins')),
    path('c/', include('src.administration.employees.urls', namespace='employees')),
    path('scheduler/', include('src.services.schedular.urls', namespace='scheduler')),
]

urlpatterns += [
    path('accounts/', include('allauth.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

""" __ DEBUG URLS __ """

if ENVIRONMENT != 'server':
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls"))
    ]
