from django.forms import ModelForm

from src.accounts.models import Employee, UserDocument, EmployeeWork, EmployeeIdPass, EmployeeHealth, EmployeeAppearance
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from src.administration.admins.models import Country

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


class CountryForm(ModelForm):

    class Meta:
        model = Country
        fields = '__all__'


""" EMPLOYEE FORMS ALL """


class EMPMGMTEmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'


class EMPMGMTEmployeeWorkForm(ModelForm):
    class Meta:
        model = EmployeeWork
        fields = '__all__'


class EMPMGMTEmployeeIdPassForm(ModelForm):
    class Meta:
        model = EmployeeIdPass
        fields = '__all__'


class EMPMGMTEmployeeHealthForm(ModelForm):
    class Meta:
        model = EmployeeHealth
        fields = '__all__'


class EMPMGMTEmployeeAppearanceForm(ModelForm):
    class Meta:
        model = EmployeeAppearance
        fields = '__all__'

