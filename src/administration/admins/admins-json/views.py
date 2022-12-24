from django.shortcuts import get_object_or_404
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from jsonview.decorators import json_view
from src.accounts.decorators import admin_protected
from src.accounts.models import Employee
from src.administration.admins.forms import (
    CountryForm, EMPMGMTEmployeeForm, EMPMGMTEmployeeWorkForm, EMPMGMTEmployeeAppearanceForm, EMPMGMTEmployeeHealthForm,
    EMPMGMTEmployeeIdPassForm, EMPMGMTEmployeeContractForm, EMPMGMTEmployeeDocumentForm, EMPMGMTEmployeeEducationForm,
    EMPMGMTEmployeeEmploymentForm, EMPMGMTEmployeeQualificationForm, EMPMGMTEmployeeTrainingForm,
    EMPMGMTEmployeeEmergencyContactForm, EMPMGMTEmployeeLanguageSkillForm
)
from src.accounts.models import (
    Employee, EmployeeContract, EmployeeDocument, EmployeeEducation, EmployeeEmployment, EmployeeQualification,
    EmployeeTraining, EmployeeLanguageSkill, EmployeeEmergencyContact, EmployeeAppearance, EmployeeHealth,
    EmployeeWork, EmployeeIdPass
)
from src.administration.admins.models import Country


@method_decorator([admin_protected, json_view], name='dispatch')
class CountryJsonView(View):

    def post(self, request, pk=None, *args, **kwargs):

        # IF Request has ID ==> MEANS UPDATE OR DELETE
        if pk:
            instance = get_object_or_404(Country, pk=pk)

            if request.GET.get('action') and request.GET.get('action') == 'DELETE':
                instance.delete()
                return {'success': True}
            else:
                form = CountryForm(instance=instance, data=request.POST)

        # IF request doesn't have any ID
        else:
            form = CountryForm(request.POST or None)

        # IF Forms are valid
        if form.is_valid():
            form.save(commit=True)
            return {'success': True}

        # Failure Response
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}


""" 
DOMAIN -> EMPLOYEE MANAGEMENT 
ACTION -> update only 
"""


@method_decorator([admin_protected, json_view, csrf_exempt], name='dispatch')
class EmployeeJsonView(View):

    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Employee, pk=pk)
        form = EMPMGMTEmployeeForm(instance=instance, data=request.POST)

        if form.is_valid():
            form.save(commit=True)
            return {'success': True}

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeWorkJsonView(View):

    def post(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(Employee, pk=pk)
        form = EMPMGMTEmployeeWorkForm(instance=instance.employeework, data=request.POST)

        if form.is_valid():
            form.save(commit=True)
            return {'success': True}

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeHealthJsonView(View):

    def post(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(Employee, pk=pk)
        form = EMPMGMTEmployeeHealthForm(instance=instance.employeehealth, data=request.POST)

        if form.is_valid():
            form.save(commit=True)
            return {'success': True}

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeAppearanceJsonView(View):

    def post(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(Employee, pk=pk)
        form = EMPMGMTEmployeeAppearanceForm(instance=instance.employeeappearance, data=request.POST)

        if form.is_valid():
            form.save(commit=True)
            return {'success': True}

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}