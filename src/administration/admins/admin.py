from django.contrib import admin
from .models import (
    Client,  Site, Position,
    ReportType, Employee, ShiftDay, Shift
)


class ShiftDayAdmin(admin.ModelAdmin):
    list_display = ['shift', 'shift_date']


class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_date', 'end_date', 'start_time', 'end_time', 'client', 'pay_rate', 'charge_rate',
                    'week_days']


admin.site.register(Position)
admin.site.register(Client)
admin.site.register(ReportType)
admin.site.register(Site)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(ShiftDay, ShiftDayAdmin)
admin.site.register(Employee)
