from django.contrib import admin
from .models import (
    Client, Asset, AssetAudit, Site, Position, Contact, FormBuilder,
    EmailAccount, Vehicle, ReportType, Qualification, Employee, ShiftDay, Shift
)


class ShiftDayAdmin(admin.ModelAdmin):
    list_display = ['shift', 'shift_date']


class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_date', 'end_date', 'start_time', 'end_time', 'client', 'pay_rate', 'charge_rate']


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
admin.site.register(Shift, ShiftAdmin)
admin.site.register(ShiftDay, ShiftDayAdmin)
admin.site.register(Employee)
