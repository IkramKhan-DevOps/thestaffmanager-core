from django.contrib.auth.models import User
from django.forms import ModelForm


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]

