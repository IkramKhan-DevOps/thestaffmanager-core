from django.db import models
from django.dispatch import receiver
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from core import settings


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

#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_statics")
# def create_user_stats(sender, instance, created, **kwargs):
#     """
#     :TOPIC if user creates at any point the statistics model will be initialized
#     :param sender:
#     :param instance:
#     :param created:
#     :param kwargs:
#     :return:
#     """
#     if created:
#         pass
