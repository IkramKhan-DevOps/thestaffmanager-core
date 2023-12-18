from datetime import datetime, timedelta

from colorfield.fields import ColorField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from src.accounts.models import Employee
from faker import Faker

User = get_user_model()
fake = Faker()


class Position(models.Model):
    name = models.CharField(max_length=255)
    card_color = ColorField(default='#FFFFFF')
    charge_rate = models.FloatField()
    pay_rate = models.FloatField()

    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Positions"

    def __str__(self):
        return str(self.name)

    @classmethod
    def fake(cls, loop=10):
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


class Department(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Departments"

    def __str__(self):
        return str(self.name)

    @classmethod
    def fake(cls, loop=10):
        print()
        print("- DEPARTMENT: build")
        for x in range(loop):
            Department.objects.create(
                name=fake.job(), is_active=True
            )
            print(f"---- department: {x} faked.")
        print("- END ")
        print()


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    time_zone = models.CharField(max_length=100, null=True, blank=True)
    phone_code = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['-id']

    def __str__(self):
        return self.name

    @classmethod
    def fake(cls, loop=10):
        print()
        print("- COUNTRY: build")
        for x in range(loop):
            Country.objects.create(
                name=fake.country()
            )
            print(f"---- country: {x} faked.")
        print("- END ")
        print()


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    registration_number = models.CharField(null=True, blank=True, max_length=255)
    vat_number = models.CharField(null=True, blank=True, max_length=255)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True, verbose_name="City/Town")
    Post_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)

    is_active = models.BooleanField(
        default=False,
        help_text="Is this client is active"
    )

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Clients"

    def __str__(self):
        return str(self.name)

    def get_sites(self):
        return Site.objects.filter(client=self)

    @classmethod
    def fake(cls, loop=10):
        print()
        print("- CLIENTS: build")
        for x in range(loop):
            Client.objects.create(
                name=fake.bs(), registration_number=fake.isbn10()
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
    def fake(cls, loop=10):
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

    company_name = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    geo_fencing_range = models.CharField(
        max_length=1000, help_text="What is the maximum distance an employee can "
                                   "be from their designated location when starting their shift? in meters."
    )

    notes = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, verbose_name='City/Town')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    check_calls_enabled = models.BooleanField(
        default=False, help_text="Enabling check calls will allow the system to track employee work during their shift."
    )
    is_active = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Sites"

    def __str__(self):
        return str(self.name)

    @classmethod
    def fake(cls, loop=10):
        print()
        print("- SITES: build")
        for x in range(loop):
            Site.objects.create(
                site_id=fake.random_number(digits=3, fix_len=False),
                latitude=fake.random_number(digits=3, fix_len=False),
                longitude=fake.random_number(digits=3, fix_len=False),
                name=fake.isbn10(),
                client=Client.objects.order_by('?').first(),
                notes=fake.paragraph(nb_sentences=3),
                description=fake.paragraph(nb_sentences=3),
                company_name=fake.bs(),
                address=fake.address(),
                city=fake.city(),
                country=Country.objects.order_by('?').first(),
                geo_fencing_range=fake.random_number(digits=5, fix_len=False),
            )
            print(f"---- Site: {x} faked.")
        print("- END ")
        print()


class Shift(models.Model):
    JOB_TYPE_CHOICE = (
        ('o', 'Open'),
        ('p', 'Pattern'),
    )
    REPEAT_POLICY_TYPE = (
        ('r', 'Regular'),
        ('w', 'Weekly repeat'),
        ('d', 'Selected Dates'),
    )
    job_type = models.CharField(default='o', choices=JOB_TYPE_CHOICE, max_length=1)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
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
        if self.job_type == 'o' or not self.end_date:
            self.end_date = self.start_date
        super(Shift, self).save(*args, **kwargs)

    def get_shifts(self):
        return ShiftDay.objects.filter(shift=self)

    def get_week_shifts_status(self):
        llist = []
        [llist.append(True) if str(x) in self.week_days else llist.append(False) for x in range(7)]
        return llist


class ShiftDay(models.Model):
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
            self.employee = self.shift.employee

        # BOTH (ON-CREATE + ON-UPDATE)
        # IF CHANGES IN END - DATE
        if self.shift_date:
            start = datetime.combine(self.shift_date, self.shift.start_time)
            end = datetime.combine(self.shift_date, self.shift.end_time)

            if start > end:
                self.shift_end_date = self.shift_date + timedelta(days=1)
            else:
                self.shift_end_date = self.shift_date

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
        if sd <= nd <= ed:

            # IF USER CLOCKED IN
            if self.clock_in:
                return "running"

            # IF USER NOT CLOCKED IN
            else:
                return "late"

        return "clash"

    def is_clock_in_correct(self):
        sd = datetime.combine(self.shift_date, self.shift_time)
        if self.clock_in:
            c_in = datetime.combine(self.shift_date, self.clock_in)
            if c_in.strftime("%I:%M%p") == sd.strftime("%I:%M%p"):
                return True
            else:
                return False
        else:
            nd = datetime.now()
            if sd >= nd:
                return True
            else:
                return False

    def is_clock_out_correct(self):
        ed = datetime.combine(self.shift_end_date, self.shift_end_time)
        if self.clock_out:
            c_out = datetime.combine(self.shift_end_date, self.clock_out)
            if c_out.strftime("%I:%M%p") == ed.strftime("%I:%M%p"):
                return True
            else:
                return False
        else:
            nd = datetime.now()
            if ed >= nd:
                return True
            else:
                return False

    def get_shift_hours(self):
        start = datetime.combine(self.shift_date, self.shift_time)
        end = datetime.combine(self.shift_end_date, self.shift_end_time)
        return round((end - start).total_seconds() / 3600)

    def get_active_hours(self):
        if self.clock_in and self.clock_out:
            start = datetime.combine(self.shift_date, self.clock_in)
            end = datetime.combine(self.shift_end_date, self.clock_out)
            return round((end - start).total_seconds() / 3600)
        return 0

    def get_extra_hours(self):
        if self.clock_in and self.clock_out:
            required = datetime.combine(self.shift_end_date, self.shift_end_time) - datetime.combine(self.shift_date,
                                                                                                     self.shift_time)
            active = datetime.combine(self.shift_end_date, self.clock_out) - datetime.combine(self.shift_date,
                                                                                              self.clock_in)
            return round((active - required).total_seconds() / 3600)
        return 0


class AbsenseType(models.Model):
    name = models.CharField(max_length=50)
    is_paid = models.BooleanField(
        default=False,
        help_text="Is this absence type considered as a paid leave"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Absense Types"

    def __str__(self):
        return self.name

    @classmethod
    def fake(cls, loop=10):
        print()
        print("- ABSENSE TYPES: build")
        for x in range(loop):
            AbsenseType.objects.create(
                name=fake.isbn10(),
            )
            print(f"---- ABSENSE TYPES: {x} faked.")
        print("- END ")
        print()


class Absense(models.Model):
    TYPE_CHOICES = (
        ('s', 'Sick Leave'),
        ('o', 'Other'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    absense_type = models.ForeignKey(AbsenseType, on_delete=models.SET_NULL, null=True, blank=False)
    date_from = models.DateField(help_text="Employee holiday starts from")
    date_to = models.DateField(help_text="Employee holiday ends on")
    comment = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Absences"

    def __str__(self):
        return self.employee.user.get_user_name() + " " + "Leave: " + str(self.pk)
