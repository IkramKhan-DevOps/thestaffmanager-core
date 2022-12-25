from django.http import Http404
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

        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeContractGenericJsonView(View):
    instance = None
    action = None
    context = {'success': True}

    def get(self, request, pk=None, *args, **kwargs):
        self.instance = get_object_or_404(EmployeeContract, pk=pk) if pk else None
        self.action = request.GET.get('action')

        if self.action == "DELETE":
            self.delete_object(request)
            return self.context

    def post(self, request, pk=None, *args, **kwargs):
        context = None
        self.instance = get_object_or_404(EmployeeContract, pk=pk) if pk else None
        self.action = request.GET.get('action')

        if self.action == "POST":
            self.add_object(request)
            return self.context
        if self.action == "PUT":
            self.add_object(request)
            return self.context

        if not context:
            raise Http404
        else:
            return context

    def add_object(self, request):
        form = EMPMGMTEmployeeContractForm(data=request.POST)
        if form.is_valid():
            form.save(commit=True)

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}

    def update_object(self, request):
        form = EMPMGMTEmployeeContractForm(data=request.POST, instance=self.instance)
        if form.is_valid():
            form.save(commit=True)

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}

    def delete_object(self, request):
        self.instance.delete()


"""

"""


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeQualificationAddJsonView(View):

    def post(self, request):
        form = EMPMGMTEmployeeQualificationForm(request.POST)
        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeQualificationDeleteJsonView(View):

    def get(self, request, pk):
        instance = get_object_or_404(EmployeeQualification, pk=pk)
        instance.delete()


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeTrainingAddJsonView(View):

    def post(self, request):
        form = EMPMGMTEmployeeTrainingForm(request.POST)
        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeTrainingDeleteJsonView(View):

    def get(self, request, pk):
        instance = get_object_or_404(EmployeeTraining, pk=pk)
        instance.delete()


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeLanguageSkillAddJsonView(View):

    def post(self, request):
        form = EMPMGMTEmployeeLanguageSkillForm(request.POST)
        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeLanguageSkillDeleteJsonView(View):

    def get(self, request, pk):
        instance = get_object_or_404(EmployeeLanguageSkill, pk=pk)
        instance.delete()


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeEmploymentAddJsonView(View):

    def post(self, request):
        form = EMPMGMTEmployeeEmploymentForm(request.POST)
        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeEmploymentDeleteJsonView(View):

    def get(self, request, pk):
        instance = get_object_or_404(EmployeeEmployment, pk=pk)
        instance.delete()


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeEducationAddJsonView(View):

    def post(self, request):
        form = EMPMGMTEmployeeEducationForm(request.POST)
        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeEducationDeleteJsonView(View):

    def get(self, request, pk):
        instance = get_object_or_404(EmployeeEducation, pk=pk)
        instance.delete()


@method_decorator([admin_protected, json_view, csrf_exempt], name='dispatch')
class EmployeeDocumentAddJsonView(View):

    def post(self, request):
        form = EMPMGMTEmployeeDocumentForm(request.POST, request.FILES)
        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}


@method_decorator([admin_protected, json_view], name='dispatch')
class EmployeeDocumentDeleteJsonView(View):

    def get(self, request, pk):
        instance = get_object_or_404(EmployeeDocument, pk=pk)
        instance.delete()


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