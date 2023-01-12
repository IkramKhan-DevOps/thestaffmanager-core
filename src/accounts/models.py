from django.db import models
from django.dispatch import receiver
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from core import settings

from faker import Faker


fake = Faker()


"""
python manage.py make migrations accounts -> apps
python manage.py migrate 
"""


""" MAIN USER """


class User(AbstractUser):
    profile_image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[100, 100], quality=75, force_format='PNG',
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    note = models.TextField(null=True, blank=True, default='')

    is_employee = models.BooleanField(default=False, help_text="Designates whether this user is employee")
    is_two_factor_auth = models.BooleanField(default=False, verbose_name="Two Factor Auth")
    is_email_verified = models.BooleanField(default=False, verbose_name="Email Verified")

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_employee_profile(self):
        if self.is_employee:
            employee = Employee.objects.filter(user=self)
            if employee:
                return employee.first()
            else:
                return Employee.objects.create(user=self)
        return None

    def is_first_or_last_name(self):
        if self.first_name or self.last_name:
            return True
        return False

    def get_user_name(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return self.username

    def get_user_documents(self):
        return UserDocument.objects.filter(user=self)

    def get_name_code(self):
        name = ""
        if self.first_name or self.last_name:
            if self.first_name:
                name += self.first_name[0]
            if self.last_name:
                name += self.last_name[0]
        else:
            name = self.username[0:2]
        return name

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)


class UserDocument(models.Model):
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='accounts/files/employees/docs/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Employee Documents"

    def __str__(self):
        return self.document_name

    def delete(self, *args, **kwargs):
        self.document_file.delete(save=True)
        super(UserDocument, self).delete(*args, **kwargs)


""" EMPLOYEE USER"""


class Employee(models.Model):
    EMPLOYEE_TYPE_CHOICE = (
        ('s', 'Service Partner'),
        ('f', 'Full Time')
    )
    EMPLOYEE_GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('t', 'Tans'),
    )

    # USER CONNECT
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=255, null=True, blank=True, help_text="Employee id must be unique")
    type = models.CharField(max_length=1, choices=EMPLOYEE_TYPE_CHOICE, default='s')
    pob = models.CharField(null=True, blank=True, max_length=255)

    # CONTACT AND ADDRESS
    phone_number_2 = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='City/Town')
    post_code = models.CharField(max_length=50, null=True, blank=True)
    country = models.ForeignKey(
        'admins.Country', max_length=255, null=True, blank=True,
        on_delete=models.CASCADE, related_name='employee_country'
    )
    nationality = models.CharField(max_length=100, null=True, blank=True)
    # GENDER AND DOB
    gender = models.CharField(max_length=1, choices=EMPLOYEE_GENDER_CHOICE, default='m')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    city_of_birth = models.CharField(null=True, blank=True, max_length=100)
    country_of_birth = models.ForeignKey(
        'admins.Country', null=True, blank=True, on_delete=models.CASCADE,
        verbose_name="Country of Birth", related_name='employee_country_of_birth'
    )

    # MANY TO MANY
    sites = models.ManyToManyField('admins.Site', blank=True, through='EmployeeSite')
    positions = models.ManyToManyField('admins.Position', blank=True, through='EmployeePosition')
    departments = models.ManyToManyField('admins.Department', blank=True, through='EmployeeDepartment')

    # CHECKS
    driver_license = models.BooleanField(default=False)
    access_to_car = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.user.username

    @classmethod
    def fake_employees(cls, loop=30):
        print()
        print("- EMPLOYEES: build")
        for x in range(loop):
            User.objects.create(
                username=fake.user_name(), first_name=fake.first_name(), last_name=fake.last_name(),
                email=fake.ascii_email(), password=f'poiuyt0987654', phone_number=fake.phone_number(),
                is_employee=True, is_active=True
            )
            print(f"---- Employee: {x} faked.")
        print("- END ")
        print()


""" EMPLOYEE USER STATS"""


class EmployeeIdPass(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    document_id = models.CharField(max_length=255, help_text="Identification or Unique ID from issuer", null=True)
    date_of_issue = models.DateField(help_text="When this document is issued to you", null=True)
    date_of_expiry = models.DateField(help_text="When this document will be expired", null=True)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Document: {self.document_id}"


class EmployeeWork(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    ni_number = models.CharField(max_length=255, null=True, blank=True)
    utr = models.CharField(max_length=255, null=True, blank=True)
    tax_code = models.CharField(null=True, blank=True, max_length=255)
    visa_required = models.BooleanField(default=False)
    visa_country = models.ForeignKey('admins.Country', null=True, blank=True, on_delete=models.SET_NULL)
    visa_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f"{self.employee.user.get_user_name()} NI: {self.ni_number}"


class EmployeeEmergencyContact(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    relation = models.CharField(max_length=255)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Relative: {self.first_name} {self.last_name}"


class EmployeeContract(models.Model):
    EMPLOYEE_TYPE = (
        ('s', 'Standard'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=1, choices=EMPLOYEE_TYPE, null=True, blank=True)
    start = models.DateField(help_text="When this Contract starts", null=True, blank=True)
    end = models.DateField(help_text="When this Contact ends", null=True, blank=True)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Contract: {self.get_type_display()}"


class EmployeeQualification(models.Model):
    TYPE_CHOICE = (
        ('fad', 'First AID'),
        ('sia', 'SIA No'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICE)
    certificate_number = models.CharField(max_length=255)
    expiry_date = models.DateField()

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Qualification: {self.get_type_display()}"


class EmployeeTraining(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    provider = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Training: {self.course}"


class EmployeeLanguageSkill(models.Model):
    LANGUAGE_CHOICE = (
        ('eng', 'English'),
        ('fre', 'French'),
        ('ger', 'German'),
        ('spa', 'Spanish'),
    )
    LEVEL_CHOICE = (
        ('nat', 'Native'),
        ('ele', 'Elementary'),
        ('int', 'Intermediate'),
        ('adv', 'Advance'),
        ('pro', 'Proficient'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=5, choices=LANGUAGE_CHOICE)
    level = models.CharField(max_length=5, choices=LEVEL_CHOICE)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Lang: {self.name}"


class EmployeeDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True, related_name="uploaded_by")
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='accounts/files/employees/docs/')

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Doc: {self.name}"


class EmployeeEmployment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, blank=True)
    employer = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    contact_phone = models.CharField(max_length=255, null=True, blank=True)
    date_form = models.DateField()
    date_to = models.DateField(null=True, blank=True)
    reason_for_leaving = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Employment at : {self.employer}"


class EmployeeEducation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, blank=True)
    institution = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255, null=True, blank=True)
    degree_obtained = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey('admins.Country', on_delete=models.SET_NULL, blank=False, null=True)
    date_form = models.DateField()
    date_to = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Graduated From: {self.institution}"


class EmployeeHealth(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, blank=True)
    is_disabled = models.CharField(default="No", help_text="Disabled no. (if registered disabled)", max_length=255)
    absent_days_in_last_year = models.PositiveIntegerField(default=0, help_text="How many days has the user been absent from work in the last 2 years due to sickness?")
    additional_comments = models.TextField(null=True, blank=True)
    other_serious_illness = models.TextField(null=True, blank=True, help_text="Details of any other illness or injuries relevant to the user")
    need_condition = models.BooleanField(default=False, help_text="Does the user have a medical condition?")
    need_carer = models.BooleanField(default=False, help_text="Does the user need to be accompanied by a carer or supporter?")
    heart_disease = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    glasses = models.BooleanField(default=False, verbose_name="Glasses or Contact Lenses")

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Health"


class EmployeeAppearance(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    bust = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True)
    hips = models.FloatField(null=True, blank=True)
    inside_leg = models.FloatField(null=True, blank=True)
    collar = models.FloatField(null=True, blank=True)

    hair_color = models.CharField(max_length=100, null=True, blank=True)
    eye_color = models.CharField(max_length=100, null=True, blank=True)
    hair_length = models.FloatField(null=True, blank=True)
    facial_hair = models.CharField(max_length=100, null=True, blank=True)

    t_shirt_size = models.FloatField(null=True, blank=True)
    jacket_size = models.FloatField(null=True, blank=True)
    hate_size = models.FloatField(null=True, blank=True)
    trouser_size = models.FloatField(null=True, blank=True)
    skirt_size = models.FloatField(null=True, blank=True)
    shoe_size = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-employee']

    def __str__(self):
        return f" {self.employee.user.get_user_name()} Appearance"


class EmployeeSite(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    site = models.ForeignKey('admins.Site', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Employee Sites"
        ordering = ['-id']

    def __str__(self):
        return f"{self.employee.user.get_user_name()} site > {self.site.name}"


class EmployeePosition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey('admins.Position', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Employee Positions"
        ordering = ['-id']

    def __str__(self):
        return f"{self.employee.user.get_user_name()} position > {self.position.name}"


class EmployeeDepartment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey('admins.Department', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Employee Departments"
        ordering = ['-id']

    def __str__(self):
        return f"{self.employee.user.get_user_name()} department > {self.department.name}"


class SubContractor(models.Model):

    name = models.CharField(max_length=255)

    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)

    street_address = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    country = models.ForeignKey('admins.Country', on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.CharField(max_length=1000, null=True, blank=True)

    positions = models.ManyToManyField('admins.Position', through='SubContractorPosition', blank=True)
    departments = models.ManyToManyField('admins.Department', through='SubContractorDepartment', blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Sub Contractors"

    def __str__(self):
        return self.name


class SubContractorPosition(models.Model):
    sub_contractor = models.ForeignKey(SubContractor, on_delete=models.CASCADE)
    position = models.ForeignKey('admins.Position', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.sub_contractor.name} position > {self.position.name}"


class SubContractorDepartment(models.Model):
    sub_contractor = models.ForeignKey(SubContractor, on_delete=models.CASCADE)
    department = models.ForeignKey('admins.Department', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Sub Contractor Departments"
        ordering = ['-id']

    def __str__(self):
        return f"{self.sub_contractor.name} department > {self.department.name}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_user_save")
def create_user_save(sender, instance, created, **kwargs):
    """
    :TOPIC if user creates at any point the statistics model will be initialized
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # IF USER IS NOT EMPLOYEE -- NOW
    if not instance.is_employee:
        if Employee.objects.filter(user=instance):
            instance.employee.delete()

    # IF USER IS NOT EMPLOYEE -- NOW
    else:
        employee, is_created = Employee.objects.get_or_create(user=instance)
        EmployeeIdPass.objects.get_or_create(employee=employee)
        EmployeeWork.objects.get_or_create(employee=employee)
        EmployeeHealth.objects.get_or_create(employee=employee)
        EmployeeAppearance.objects.get_or_create(employee=employee)
