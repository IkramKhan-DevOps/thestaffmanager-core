from django.contrib import admin
from .models import (
    Client, Asset, AssetAudit, Site, Position, Contact, FormBuilder,
    EmailAccount, Vehicle, ReportType, Qualification
)


admin.site.register(Position)
admin.site.register(Client)
admin.site.register(Asset)
admin.site.register(AssetAudit)
admin.site.register(Contact)
admin.site.register(FormBuilder)
admin.site.register(EmailAccount)
admin.site.register(Vehicle)
admin.site.register(ReportType)
admin.site.register(Qualification)
admin.site.register(Site)
