from colorfield.fields import ColorField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.accounts.models import User, Employee


class Position(models.Model):

    name = models.CharField(max_length=255)
    card_color = ColorField()
    charge_rate = models.FloatField()
    pay_rate = models.FloatField()

    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Positions"

    def __str__(self):
        return str(self.name)


class Client(models.Model):

    name = models.CharField(max_length=255)
    parent_client = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    xero_contact_name = models.CharField(
        max_length=255, verbose_name='Xero Contact Name - must exactly match the value specified in Xero'
    )

    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Clients"

    def __str__(self):
        return str(self.name)


class ReportType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Report Types"

    def __str__(self):
        return str(self.name)


class Site(models.Model):
    CHECK_CALLS_ENABLE_TYPE = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    site_id = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    check_calls_enable = models.CharField(max_length=5, default='no', choices=CHECK_CALLS_ENABLE_TYPE)
    camera_system_url = models.URLField(null=True, blank=True)

    notes = models.TextField(null=True, blank=True)

    company_name = models.CharField(max_length=255, null=True, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255, verbose_name='City/Town')
    Country = models.CharField(max_length=255)
    geo_fencing_range = models.CharField(max_length=1000)

    enable_day_check_ins = models.BooleanField(default=True)
    enable_night_check_ins = models.BooleanField(default=True)
    check_in_day_start = models.TimeField()
    check_in_night_start = models.TimeField()
    check_in_day_frequency_min_minutes = models.FloatField()
    check_in_day_frequency_max_minutes = models.FloatField()
    check_in_night_frequency_min_minutes = models.FloatField()
    check_in_night_frequency_max_minutes = models.FloatField()
    enable_first_shift_confirmation = models.BooleanField(default=False)
    enable_second_shift_confirmation = models.BooleanField(default=False)
    first_shift_confirmation_minutes_before = models.FloatField()  # show when upper active
    second_shift_confirmation_minutes_before = models.FloatField()  # show when upper active

    assignment_instructions = models.FileField(
        upload_to='administration/admins/documents/assignments', null=True, blank=True
    )

    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Sites"

    def __str__(self):
        return str(self.name)


class Shift(models.Model):
    JOB_TYPE_CHOICE = (
        ('shift', 'Shift'),
        ('response', 'Response'),
    )
    REPEAT_POLICY_TYPE = (
        ('r', 'Regular'),
        ('w', 'Weekly repeat'),
        ('d', 'Selected Dates'),
    )

    job_type = models.CharField(default='shift', choices=JOB_TYPE_CHOICE, max_length=50)

    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    # TODO:NOTE: on response type position is not required
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee")
    pay_rate = models.FloatField(default=0)
    charge_rate = models.FloatField(default=0)
    extra_charges = models.FloatField(default=0)
    week_days = models.CharField(max_length=7, default='', blank=True, editable=False)

    repeat_policy = models.CharField(max_length=1, default='r', choices=REPEAT_POLICY_TYPE, null=True, blank=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Shifts"

    def __str__(self):
        return str(self.pk)

    def get_shifts(self):
        return ShiftDay.objects.filter(shift=self)

    def get_week_shifts_status(self):

        llist = []
        [llist.append(True) if str(x) in self.week_days else llist.append(False) for x in range(7)]
        return llist


class ShiftDay(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    shift_date = models.DateField()

    class Meta:
        verbose_name_plural = "Shift Days"

    def __str__(self):
        return str(self.pk)
