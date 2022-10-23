import django_filters
from django.forms import TextInput

from src.administration.admins.models import Shift


class ShiftFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'ID'}), lookup_expr='icontains')

    class Meta:
        model = Shift
        fields = {
            'client': ['exact'], 'site': ['exact'], 'employee': ['exact']
        }
