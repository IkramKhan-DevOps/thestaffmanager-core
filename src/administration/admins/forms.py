from django.forms import ModelForm

from src.accounts.models import Employee, UserDocument
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


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


class UserDocumentForm(ModelForm):

    class Meta:
        model = UserDocument
        fields = [
            'document_name', 'document_file'
        ]


class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = [
            'employee_id', 'type', 'address'
        ]


class EmployeeUserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2'
        ]


class StaffUserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2'
        ]

