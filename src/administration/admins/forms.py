from django.forms import ModelForm

from src.accounts.models import User, Employee


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]


class ShiftForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'


class EmployeeCreateForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user', 'is_internal_employee'
        ]
