
from django.contrib import admin
from django.shortcuts import redirect
from django.template.defaulttags import url
from django.urls import path, include

from django.conf import settings
from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from django.views.static import serve
from django.conf.urls.static import static


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

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

