from django.contrib import admin
from .models import (
    Client,  Site, Position,
    ReportType, Employee, ShiftDay, Shift, Country, AbsenseType, Absense
)


class ShiftDayAdmin(admin.ModelAdmin):
    list_display = ['shift', 'employee', 'shift_date', 'shift_end_date', 'clock_in', 'clock_out']


class ShiftAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'start_date', 'end_date', 'start_time', 'end_time', 'employee', 'pay_rate', 'charge_rate'
    ]


class CountryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'language', 'currency', 'time_zone', 'phone_code', 'is_active'
    ]


admin.site.register(Site)
admin.site.register(Client)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(ReportType)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ShiftDay, ShiftDayAdmin)
admin.site.register(AbsenseType)
admin.site.register(Absense)
