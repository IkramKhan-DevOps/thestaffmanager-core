from crispy_forms.helper import FormHelper
from django.forms import ModelForm, DateInput

from src.administration.admins.models import Shift
from crispy_forms.layout import Layout, Row, Column, Div, Submit


class Row(Div):
    css_class = "row"


class ShiftModelForm(ModelForm):
    class Meta:
        model = Shift
        fields = [
            'job_type', 'repeat_policy', 'start_date', 'end_date', 'start_time', 'end_time',
            'site', 'position', 'employee', 'pay_rate', 'charge_rate', 'extra_charges'
        ]
        widgets = {
            'start_date':  DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'start_time': DateInput(attrs={'type': 'time'}),
            'end_time': DateInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['site'].widget.attrs.update({'class': 'form-control'})
        self.fields['position'].widget.attrs.update({'class': 'form-control'})
        self.fields['employee'].widget.attrs.update({'class': 'form-control'})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('job_type', css_class='col-sm-6 '),
                Column('repeat_policy', css_class='col-sm-6 '),
                Column('start_date', css_class='col-sm-3 '),
                Column('end_date', css_class='col-sm-3 '),
                Column('start_time', css_class='col-sm-3 '),
                Column('end_time', css_class='col-sm-3 '),
                Column('site', css_class='col-sm-4 '),
                Column('position', css_class='col-sm-4 '),
                Column('employee', css_class='col-sm-4 '),
                Column('pay_rate', css_class='col-sm-4 '),
                Column('charge_rate', css_class='col-sm-4 '),
                Column('extra_charges', css_class='col-sm-4 '),
            ),
        )
