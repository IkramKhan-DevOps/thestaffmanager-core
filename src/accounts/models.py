from django.db import models
from django.dispatch import receiver
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from core import settings

from faker import Faker
fake = Faker()


class User(AbstractUser):
    profile_image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[100, 100], quality=75, force_format='PNG',
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    is_employee = models.BooleanField(default=False, help_text="Designates whether this user is employee")

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_employee_profile(self):
        if self.is_employee:
            return Employee.objects.get_or_create(user=self)
        return None

    def get_user_name(self):
        print(self.username)
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return self.username

    def get_user_documents(self):
        return UserDocument.objects.filter(user=self)

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)


class Employee(models.Model):
    EMPLOYEE_TYPE_CHOICE = (
        ('s', 'Service Partner'),
        ('f', 'Full Time')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=255, null=True, blank=True, help_text="Employee id must be unique")
    employee_type = models.CharField(max_length=1, choices=EMPLOYEE_TYPE_CHOICE, default='s')
    is_internal_employee = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.user.username

    @classmethod
    def fake_employees(cls, loop=10):
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
    if created:
        if instance.is_employee:
            Employee.objects.create(user=instance)
