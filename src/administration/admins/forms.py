from django.forms import ModelForm

from src.accounts.models import User, Employee


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'profile_image', 'username', 'first_name', 'last_name', 'email', 'phone_number'
        ]


class ShiftForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'employee_type', 'is_internal_employee'
        ]