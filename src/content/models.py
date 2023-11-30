from django.core.exceptions import ValidationError
from django.db import models
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField


""" VALIDATORS """


# TODO: FIX - required.
def single_record_validation(value):
    if Application.objects.count() > 0:
        return ValidationError("You aren't allowed to add more than one record")
    return value


""" MODELS """


class Application(models.Model):
    name = models.CharField(
        max_length=255, unique=True, default='_name_', validators=[single_record_validation]
    )
    tagline = models.CharField(max_length=255, default='_no tagline_')
    description = models.TextField(default='_no description provided_')
    logo = ResizedImageField(
        upload_to='content/logo/', null=True, blank=True, size=[500, 500],
        quality=75, force_format='PNG', crop=['middle', 'center'],
        help_text='size of logo must be 500*500 and format must be png image file'
    )

    contact_number = PhoneNumberField(default="+923000000000")
    contact_email = models.EmailField(default='support@site.com')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

