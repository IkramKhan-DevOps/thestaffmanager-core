import django_filters
from django.forms import TextInput

from src.accounts.models import User
from src.administration.admins.models import Shift, Client, Site, ShiftDay


class ShiftFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Shift ID'}), lookup_expr='icontains')

    class Meta:
        model = Shift
        fields = {
            'client': ['exact'], 'site': ['exact'], 'employee': ['exact']
        }


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {'is_active', 'is_employee'}


class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'name'}), lookup_expr='icontains')
    xero_contact_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'xero contact name'}), lookup_expr='icontains')

    class Meta:
        model = Client
        fields = {'is_active'}


class SiteFilter(django_filters.FilterSet):
    site_id = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Site ID'}), lookup_expr='icontains')
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Site name'}), lookup_expr='icontains')
    company_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Company name'}), lookup_expr='icontains')

    class Meta:
        model = Site
        fields = {'is_active'}


class ShiftDayFilter(django_filters.FilterSet):
    shift_date = django_filters.DateRangeFilter()
    shift__employee__user__username = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ShiftDay
        fields = {
        }

