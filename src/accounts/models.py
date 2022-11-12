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

    is_employee = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
