from datetime import datetime, timedelta

from colorfield.fields import ColorField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.accounts.models import User, Employee

from faker import Faker

fake = Faker()


class Position(models.Model):
    name = models.CharField(max_length=255)
    card_color = ColorField()
    charge_rate = models.FloatField()
    pay_rate = models.FloatField(help_text="Please provide payments")

    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Positions"

    def __str__(self):
        return str(self.name)

    @classmethod
    def fake_position(cls, loop=10):
        print()
        print("- POSITIONS: build")
        for x in range(loop):
            Position.objects.create(
                name=fake.job(), card_color="#FFFFFF", charge_rate=fake.random_number(digits=3),
                pay_rate=fake.random_number(digits=3)
            )
            print(f"---- Position: {x} faked.")
        print("- END ")
        print()


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

    def get_sites(self):
        return Site.objects.filter(client=self)

    @classmethod
    def fake_client(cls, loop=10):
        print()
        print("- CLIENTS: build")
        for x in range(loop):
            Client.objects.create(
                name=fake.bs(), xero_contact_name=fake.isbn10()
            )
            print(f"---- Client: {x} faked.")
        print("- END ")
        print()


class ReportType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Report Types"

    def __str__(self):
        return str(self.name)

    @classmethod
    def fake_report_type(cls, loop=10):
        print()
        print("- REPORT TYPE: build")
        for x in range(loop):
            ReportType.objects.create(
                name=fake.bs(), icon="fa fa-icon"
            )
            print(f"---- Report Type: {x} faked.")
        print("- END ")
        print()


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
    country = models.CharField(max_length=255)
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

    @classmethod
    def fake_site(cls, loop=10):
        print(fake.country())
        print()
        print("- SITES: build")
        for x in range(loop):
            Site.objects.create(
                site_id=fake.random_number(digits=3, fix_len=False),
                name=fake.isbn10(),
                client=Client.objects.order_by('?').first(),
                check_calls_enable=fake.pybool(),
                camera_system_url=f"https://example.com/{fake.ean(length=13)}/",
                notes=fake.paragraph(nb_sentences=3),
                company_name=fake.bs(),
                address_line_1=fake.address(),
                address_line_2=fake.address(),
                city=fake.city(),
                country=fake.country(),
                geo_fencing_range=fake.random_number(digits=5, fix_len=False),
                enable_day_check_ins=fake.pybool(),
                enable_night_check_ins=fake.pybool(),
                check_in_day_start=fake.date_time(),
                check_in_night_start=fake.date_time(),
                first_shift_confirmation_minutes_before=fake.random_number(digits=2, fix_len=False),
                second_shift_confirmation_minutes_before=fake.random_number(digits=2, fix_len=False),
                check_in_day_frequency_min_minutes=fake.random_number(digits=2, fix_len=False),
                check_in_day_frequency_max_minutes=fake.random_number(digits=2, fix_len=False),
                check_in_night_frequency_min_minutes=fake.random_number(digits=2, fix_len=False),
                check_in_night_frequency_max_minutes=fake.random_number(digits=2, fix_len=False),
                enable_first_shift_confirmation=fake.pybool(),
                enable_second_shift_confirmation=fake.pybool(),
            )
            print(f"---- Site: {x} faked.")
        print("- END ")
        print()


class Shift(models.Model):
    """
    TODO: UPDATE
    1. quantity : not required
    2. job_type : data changed
    3. on_create: on shift create > create history record
    """

    JOB_TYPE_CHOICE = (
        ('o', 'Open'),
        ('p', 'Pattern'),
    )
    REPEAT_POLICY_TYPE = (
        ('r', 'Regular'),
        ('w', 'Weekly repeat'),
        ('d', 'Selected Dates'),
    )
    job_type = models.CharField(default='p', choices=JOB_TYPE_CHOICE, max_length=1)

    start_date = models.DateField()
    end_date = models.DateField(null=False, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee")

    # quantity = models.PositiveIntegerField(default=1)
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

    def save(self, *args, **kwargs):
        """
        LOGIC 1 :: if job_type == open >> set last_date to first_date
        """
        if self.job_type == 'o' and self.start_date:
            self.end_date = self.start_date
        super(Shift, self).save(*args, **kwargs)

    def get_shifts(self):
        return ShiftDay.objects.filter(shift=self)

    def get_week_shifts_status(self):
        llist = []
        [llist.append(True) if str(x) in self.week_days else llist.append(False) for x in range(7)]
        return llist


class ShiftDay(models.Model):
    """
    TODO: UPDATE
    add    > employee here to ? shift can be assigned to someone else
    add    > shift_start_time
    add    > shift_end_time
    add    > shift_start_date
    add    > shift_end_date
    remove > shift, worked and extra hours
    """

    STATUS_CHOICE = (
        ('awa', 'Awaiting'),
        ('run', 'Running'),
        ('com', 'Completed'),
        ('mis', 'Missed'),
    )
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee_for_shift"
    )

    shift_date = models.DateField()
    shift_end_date = models.DateField()

    shift_time = models.TimeField(null=True, blank=True)
    shift_end_time = models.TimeField(null=True, blank=True)

    shift_hours = models.PositiveIntegerField(default=0)
    worked_hours = models.PositiveIntegerField(default=0)
    extra_hours = models.IntegerField(default=0)

    status = models.CharField(max_length=3, default="awa", choices=STATUS_CHOICE)

    class Meta:
        verbose_name_plural = "Shift Days"

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        """
        :start       --- get start datetime from (shift_date + shift_start_time)
        :end         --- get start datetime from (shift_date + shift_end_time)
        :total hours --- end - start
        """

        # ON CREATE :: shift_times and shift_dates are equal to parent
        if self._state.adding and self.shift_date:
            self.shift_time = self.shift.start_time
            self.shift_end_time = self.shift.end_time
            self.shift_date = self.shift.start_date
            self.shift_end_date = self.shift.end_date
            self.employee = self.shift.employee

        # BOTH (ON-CREATE + ON-UPDATE)
        # IF CHANGES IN END - DATE
        if self.shift_date:
            start = datetime.combine(self.shift_date, self.shift.start_time)
            end = datetime.combine(self.shift_date, self.shift.end_time)

            if start > end:
                self.shift_end_date = self.shift_date + timedelta(days=1)
                end = datetime.combine(self.shift_end_date, self.shift.end_time)
                self.shift_hours = round((end - start).total_seconds() / 3600)
            else:
                self.shift_end_date = self.shift_date
                self.shift_hours = round((end - start).total_seconds() / 3600)

            # if self.clock_out and self.clock_in:
            #     self.worked_hours = round((self.clock_out - self.clock_in).total_seconds() / 3600)
            #     self.extra_hours = self.worked_hours - self.shift_hours

        super(ShiftDay, self).save(*args, **kwargs)

    def get_current_status(self):
        """
        1. Awaiting ::
           IF (start_date + start_time) > current time
        2. Late ::
           IF (start_date + start_time) <= now
           IF (end_date + start_time) >= now
           IF (not clocked in)
        3. Running ::
           IF (clocked in)
           IF (not clocked out)
           IF (end_date + end_time) <= now
        4. Overtime ::
           IF (clocked in)
           IF (not clocked out)
           IF (end_date + end_time) > now
        4. Completed ::
           IF (clocked out)

        :return status :
        """
        sd = datetime.combine(self.shift_date, self.shift_time)
        ed = datetime.combine(self.shift_end_date, self.shift_end_time)
        nd = datetime.now()

        # BEFORE START
        if nd < sd:
            return "awaiting"

        # AFTER END
        if nd > ed:

            # IF USER CLOCKED OUT
            if self.clock_out:
                return "completed"

            # IF USER NOT CLOCKED OUT
            else:

                # IF USER CLOCKED IN
                if self.clock_in:
                    return "overtime"

                # IF USER NOT CLOCKED IN
                else:
                    return "absent"

        # IN BETWEEN
        if sd <= nd >= ed:

            # IF USER CLOCKED IN
            if self.clock_in:
                return "running"

            # IF USER NOT CLOCKED IN
            else:
                return "late"

        return "clash"



