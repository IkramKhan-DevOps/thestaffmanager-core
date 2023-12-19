from django.forms import ModelForm

from src.administration.admins.models import Shift


class ShiftModelForm(ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'
