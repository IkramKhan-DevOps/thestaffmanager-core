from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from .settings import MEDIA_ROOT, STATIC_ROOT
from django.views.static import serve


def home_view(request):
    return redirect('accounts:login')


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('a/', include('src.administration.admins.urls', namespace='admins')),
    path('s/', include('src.administration.staff.urls', namespace='staffs')),
    path('', home_view, name='home')
]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

