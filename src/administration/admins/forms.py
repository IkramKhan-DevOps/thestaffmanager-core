from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field, Submit, Div, Column
from django.forms import ModelForm, TextInput

from src.accounts.models import (
    Employee, UserDocument, EmployeeWork, EmployeeIdPass, EmployeeHealth, EmployeeAppearance,
    EmployeeContract, EmployeeDocument, EmployeeEducation, EmployeeEmployment, EmployeeQualification, EmployeeTraining,
    EmployeeLanguageSkill, EmployeeEmergencyContact, SubContractor
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from src.administration.admins.models import Country, Absense, AbsenseType, Shift

User = get_user_model()


class Row(Div):
    css_class = "row"


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'profile_image', 'username', 'first_name', 'last_name', 'email', 'phone_number'
        ]


class ShiftForm(ModelForm):
    class Meta:
        model = Shift
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


class AbsenseTypeForm(ModelForm):

    class Meta:
        model = AbsenseType
        fields = '__all__'


class AbsenseForm(ModelForm):

    class Meta:
        model = Absense
        fields = '__all__'


class SubContractorForm(ModelForm):

    class Meta:
        model = SubContractor
        fields = '__all__'
        exclude = ['positions', 'departments']


""" EMPLOYEE FORMS ALL """


class EMPMGMTEmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user', 'sites', 'positions', 'departments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({"class": "form-control"})
        self.fields['country'].widget.attrs.update({"class": "form-control"})
        self.fields['gender'].widget.attrs.update({"class": "form-control"})
        self.fields['country_of_birth'].widget.attrs.update({"class": "form-control"})
        self.fields['driver_license'].widget.attrs.update({"class": "form-check-input"})
        self.fields['access_to_car'].widget.attrs.update({"class": "form-check-input"})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employee_id', css_class='form-group col-md-6 mb-3'),
                Column('type', css_class=' col-md-6 mb-3'),
                Column('pob', css_class='form-group col-md-6 mb-3'),
                Column('phone_number_2', css_class='form-group col-md-6 mb-3'),
                Column('address', css_class='form-group col-md-12 mb-3'),
                Column('city', css_class='form-group col-md-4 mb-3'),
                Column('post_code', css_class='form-group col-md-4 mb-3'),
                Column('country', css_class='col-md-4 mb-3'),
                Column('nationality', css_class='form-group col-md-6 mb-3'),
                Column('gender', css_class='col-md-6 mb-3'),
                Column('date_of_birth', css_class='form-group col-md-4 mb-3'),
                Column('city_of_birth', css_class='form-group col-md-4 mb-3'),
                Column('country_of_birth', css_class='col-md-4 mb-3'),
                Column('driver_license', css_class='form-check form-switch col-md-6 mb-3'),
                Column('access_to_car', css_class='form-check form-switch col-md-6 mb-3'),
            ),

        )


class EMPMGMTEmployeeWorkForm(ModelForm):
    class Meta:
        model = EmployeeWork
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['visa_required'].widget.attrs.update({'class': "form-check-input"})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('ni_number', css_class='form-group col-md-6 mb-3'),
                Column('utr', css_class='form-group col-md-6 mb-3'),
                Column('tax_code', css_class='form-group col-md-12 mb-3'),
                Column('visa_required', css_class='form-check form-switch col-md-6 mb-3'),
            ),

        )


class EMPMGMTEmployeeIdPassForm(ModelForm):
    class Meta:
        model = EmployeeIdPass
        fields = '__all__'
        exclude = ['employee']


class EMPMGMTEmployeeHealthForm(ModelForm):
    class Meta:
        model = EmployeeHealth
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['need_condition'].widget.attrs.update({'class': "form-check-input"})
        self.fields['need_carer'].widget.attrs.update({'class': "form-check-input"})
        self.fields['heart_disease'].widget.attrs.update({'class': "form-check-input"})
        self.fields['diabetes'].widget.attrs.update({'class': "form-check-input"})
        self.fields['glasses'].widget.attrs.update({'class': "form-check-input"})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                'is_disabled', 'absent_days_in_last_year', 'additional_comments',
                'other_serious_illness',
                Column('need_condition', css_class='form-check form-switch col-md-6 mb-3'),
                Column('need_carer', css_class='form-check form-switch col-md-6 mb-3'),
                Column('glasses', css_class='form-check form-switch col-md-6 mb-3'),
                Column('heart_disease', css_class='form-check form-switch col-md-4 mb-3'),
                Column('diabetes', css_class='form-check form-switch col-md-4 mb-3'),
            ),

        )


class EMPMGMTEmployeeAppearanceForm(ModelForm):
    class Meta:
        model = EmployeeAppearance
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('height', css_class=' col-md-4 mb-3'),
                Column('weight', css_class='form-group col-md-4 mb-3'),
                Column('bust', css_class='form-group col-md-4 mb-3'),
                Column('waist', css_class='form-group col-md-4 mb-3'),
                Column('chest', css_class='form-group col-md-4 mb-3'),
                Column('hips', css_class='form-group col-md-4 mb-3'),
                Column('inside_leg', css_class='form-group col-md-4 mb-3'),
                Column('collar', css_class='form-group col-md-4 mb-3'),
                Column('hair_color', css_class='form-group col-md-4 mb-3'),
                Column('eye_color', css_class='form-group col-md-4 mb-3'),
                Column('hair_length', css_class='form-group col-md-4 mb-3'),
                Column('facial_hair', css_class='form-group col-md-4 mb-3'),
                Column('t_shirt_size', css_class='form-group col-md-4 mb-3'),
                Column('jacket_size', css_class='form-group col-md-4 mb-3'),
                Column('hate_size', css_class='form-group col-md-4 mb-3'),
                Column('trouser_size', css_class='form-group col-md-4 mb-3'),
                Column('skirt_size', css_class='form-group col-md-4 mb-3'),
                Column('shoe_size', css_class='form-group col-md-4 mb-3'),
            ),

        )


""" ------ """


class EMPMGMTEmployeeContractForm(ModelForm):
    class Meta:
        model = EmployeeContract
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': "form-control"})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('type', css_class=' col-md-12 mb-3'),
                Column('start', css_class='form-group col-md-6 mb-3'),
                Column('end', css_class='form-group col-md-6 mb-3'),
            ),

        )


class EMPMGMTEmployeeDocumentForm(ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = '__all__'
        exclude = ['employee', 'uploaded_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'class': "form-control"})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-3'),
                Column('file', css_class='form-group col-md-12 mb-3'),
            ),

        )


class EMPMGMTEmployeeEducationForm(ModelForm):
    class Meta:
        model = EmployeeEducation
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': "form-control"})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('institution', css_class=' col-md-12 mb-3'),
                Column('speciality', css_class='form-group col-md-6 mb-3'),
                Column('degree_obtained', css_class='form-group col-md-6 mb-3'),
                Column('city', css_class='form-group col-md-6 mb-3'),
                Column('country', css_class='form-group col-md-6 mb-3'),
                Column('date_form', css_class='form-group col-md-6 mb-3'),
                Column('date_to', css_class='form-group col-md-6 mb-3'),
            ),

        )


class EMPMGMTEmployeeEmploymentForm(ModelForm):
    class Meta:
        model = EmployeeEmployment
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employer', css_class=' col-md-6 mb-3'),
                Column('position', css_class='form-group col-md-6 mb-3'),
                Column('contact_person', css_class='form-group col-md-6 mb-3'),
                Column('contact_phone', css_class='form-group col-md-6 mb-3'),
                Column('date_form', css_class='form-group col-md-6 mb-3'),
                Column('date_to', css_class='form-group col-md-6 mb-3'),
                Column('description', css_class='form-group col-md-6 mb-3'),
                Column('reason_for_leaving', css_class='form-group col-md-6 mb-3'),
            ),
        )


class EMPMGMTEmployeeQualificationForm(ModelForm):
    class Meta:
        model = EmployeeQualification
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': "form-control"})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('type', css_class=' col-md-12 mb-3'),
                Column('certificate_number', css_class='form-group col-md-6 mb-3'),
                Column('expiry_date', css_class='form-group col-md-6 mb-3'),
            ),
        )


class EMPMGMTEmployeeTrainingForm(ModelForm):
    class Meta:
        model = EmployeeTraining
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('provider', css_class=' col-md-12 mb-3'),
                Column('course', css_class='form-group col-md-12 mb-3'),
                Column('start_date', css_class='form-group col-md-6 mb-3'),
                Column('end_date', css_class='form-group col-md-6 mb-3'),
            ),
        )


class EMPMGMTEmployeeLanguageSkillForm(ModelForm):
    class Meta:
        model = EmployeeLanguageSkill
        fields = '__all__'
        exclude = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['level'].widget.attrs.update({'class': 'form-control'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class=' col-md-6 mb-3'),
                Column('level', css_class='form-group col-md-6 mb-3'),
            ),
        )


class EMPMGMTEmployeeEmergencyContactForm(ModelForm):
    class Meta:
        model = EmployeeEmergencyContact
        fields = '__all__'
        exclude = ['employee']


class EMPMGMTUserNotesForm(ModelForm):
    class Meta:
        model = User
        fields = ['note']
