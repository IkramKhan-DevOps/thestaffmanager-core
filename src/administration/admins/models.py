from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Position(models.Model):
    color_image_choice = models.ImageField(upload_to="images")

    name = models.CharField(max_length=255)
    card_color = ColorField(image_field="color_image_choice")
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
    xero_contact_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Clients"

    def __str__(self):
        return str(self.name)


class Contact(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=11)

    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Contacts"

    def __str__(self):
        return str(self.user)


class Site(models.Model):
    pass


class Asset(models.Model):
    pass


class Qualification(models.Model):
    pass


class ReportType(models.Model):
    pass


class Vehicle(models.Model):
    pass


class EmailAccount(models.Model):
    pass


class FormBuilder(models.Model):
    pass


class AssetAudit(models.Model):
    pass
