from django.contrib import admin

from src.content.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline', 'contact_number', 'contact_email']

