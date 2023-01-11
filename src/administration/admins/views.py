import json
from calendar import monthrange

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, DeleteView,
    CreateView)

from core.settings import SYS_VERIFICATION_EMAILS
from .bll import shifts_create_update
from .filters import ShiftFilter, UserFilter, ClientFilter, SiteFilter, ShiftDayFilter
from .forms import (
    EmployeeForm, UserDocumentForm, EmployeeUserCreateForm, StaffUserCreateForm, CountryForm,

    EMPMGMTEmployeeForm, EMPMGMTEmployeeWorkForm, EMPMGMTEmployeeAppearanceForm, EMPMGMTEmployeeHealthForm,
    EMPMGMTEmployeeIdPassForm,

    EMPMGMTEmployeeContractForm, EMPMGMTEmployeeDocumentForm, EMPMGMTEmployeeEducationForm,
    EMPMGMTEmployeeEmploymentForm, EMPMGMTEmployeeQualificationForm, EMPMGMTEmployeeTrainingForm,
    EMPMGMTEmployeeEmergencyContactForm, EMPMGMTEmployeeLanguageSkillForm,
    EMPMGMTUserNotesForm, ShiftForm, SubContractorForm
)
from .mail import sent_email_over_employee_create
from .models import (
    Position, Client, Site, ReportType, Shift, ShiftDay, Employee, Country, Department, AbsenseType, Absense,
)
import datetime

from src.accounts.decorators import admin_protected
from src.accounts.models import (
    User,
    EmployeeIdPass, EmployeeWork, EmployeeHealth, EmployeeAppearance,
    EmployeeContract, EmployeeDocument, EmployeeEducation, EmployeeEmployment, EmployeeQualification,
    EmployeeTraining, EmployeeLanguageSkill, EmployeeEmergencyContact, EmployeeSite, SubContractor
)

""" MAIN """


@method_decorator([admin_protected, never_cache], name='dispatch')
class ScheduleView(TemplateView):
    template_name = 'admins/schedule.html'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)

        def get_query_over_request(_request):
            # DEFAULT: query year and month
            _current_month = datetime.date.today().month
            _current_year = datetime.date.today().year
            shifts_queryset = ShiftDay.objects.filter(
                Q(shift_date__month=datetime.date.today().month, shift_date__year=datetime.date.today().year)
            ).values(
                'id', 'shift_id', 'shift__start_time', 'shift__end_time', 'shift_date',
                'shift__employee', 'shift__employee_id', 'shift__site__name'
            )

            # CHECK1: if request contains date in get
            requested_month = _request.GET.get('month')
            requested_year = _request.GET.get('year')
            search = self.request.GET.get('search')
            _employees = Employee.objects.all()
            if search:
                _employees = _employees.filter(user__username__icontains=search)

            if (requested_month and 0 < int(requested_month) < 13) and \
                    (requested_year and int(requested_year) > 0):
                shifts_queryset = ShiftDay.objects.filter(
                    Q(shift_date__month=datetime.date.today().month,
                      shift_date__year=datetime.date.today().year)
                ).values(
                    'id', 'shift_id', 'shift__start_time', 'shift__end_time',
                    'shift_date'
                )
                _current_year = requested_year
                _current_month = requested_month if int(requested_month) > 9 else "0" + requested_month

            return shifts_queryset, _current_month, _current_year, _employees

        # CALL: get month, year and query over it
        shifts, current_month, current_year, employees = get_query_over_request(self.request)

        # CONTEXT: data
        context['shifts'] = shifts
        context['shift_form'] = ShiftForm()
        context['employees'] = employees
        context['current_day'] = datetime.date.today().day
        context['current_month'] = current_month
        context['current_year'] = current_year
        context['current_date'] = datetime.date.today()

        return context


@method_decorator([admin_protected], name='dispatch')
class AbsenseScheduleView(ListView):
    queryset = Absense
    template_name = 'admins/absense_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_days = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
        context['days'] = list(range(1, num_days + 1))
        context['employees'] = Employee.objects.all()
        context['absent_types'] = AbsenseType.objects.all()
        return context


@method_decorator([admin_protected], name='dispatch')
class CheckCallsView(TemplateView):
    template_name = '000.html'


@method_decorator(admin_protected, name='dispatch')
class TimeClockView(ListView):
    template_name = 'admins/time_clock.html'

    def get_queryset(self):
        return ShiftDay.objects.all().order_by('-shift_date', '-clock_in', '-shift_end_date', '-clock_out')

    def get_context_data(self, **kwargs):
        context = super(TimeClockView, self).get_context_data(**kwargs)

        filter_object = ShiftDayFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = filter_object.form

        paginator = Paginator(filter_object.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(admin_protected, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['shifts_days'] = ShiftDay.objects.filter(shift_date=datetime.datetime.now())
        context['shifts_all'] = Shift.objects.count()
        context['sites_all'] = Site.objects.count()
        context['employees_all'] = Employee.objects.count()
        context['clients_all'] = Client.objects.count()

        return context


@method_decorator(admin_protected, name='dispatch')
class PositionListView(ListView):
    queryset = Position.objects.all()


@method_decorator(admin_protected, name='dispatch')
class PositionCreateView(CreateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('admins:position-list')


@method_decorator(admin_protected, name='dispatch')
class PositionUpdateView(UpdateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('admins:position-list')


@method_decorator(admin_protected, name='dispatch')
class PositionDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy('admins:position-list')


@method_decorator(admin_protected, name='dispatch')
class CountryListView(ListView):
    queryset = Country.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['form'] = CountryForm()
        return context


@method_decorator(admin_protected, name='dispatch')
class CountryCreateView(CreateView):
    model = Country
    fields = '__all__'
    success_url = reverse_lazy('admins:country-list')


@method_decorator(admin_protected, name='dispatch')
class CountryUpdateView(UpdateView):
    model = Country
    fields = '__all__'
    success_url = reverse_lazy('admins:country-list')


@method_decorator(admin_protected, name='dispatch')
class CountryDeleteView(DeleteView):
    model = Country
    success_url = reverse_lazy('admins:country-list')


@method_decorator(admin_protected, name='dispatch')
class DepartmentListView(ListView):
    queryset = Department.objects.all()


@method_decorator(admin_protected, name='dispatch')
class DepartmentCreateView(CreateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('admins:department-list')


@method_decorator(admin_protected, name='dispatch')
class DepartmentUpdateView(UpdateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('admins:department-list')


@method_decorator(admin_protected, name='dispatch')
class DepartmentDetailView(DetailView):
    model = Department


@method_decorator(admin_protected, name='dispatch')
class DepartmentDeleteView(DeleteView):
    model = Department
    success_url = reverse_lazy('admins:department-list')


""" STUDENT CLASS """


@method_decorator(admin_protected, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.all()
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        _filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(admin_protected, name='dispatch')
class UserStaffCreateView(CreateView):
    model = User
    form_class = StaffUserCreateForm
    template_name = 'admins/user_create_form.html'
    success_url = reverse_lazy('admins:user-list')

    def form_valid(self, form):
        form.instance.is_staff = True
        return super().form_valid(form)


@method_decorator(admin_protected, name='dispatch')
class UserEmployeeCreateView(CreateView):
    model = User
    form_class = EmployeeUserCreateForm
    template_name = 'admins/user_create_form.html'
    success_url = reverse_lazy('admins:user-list')

    def form_valid(self, form):
        username = str(form.instance.email).split('@')[0]
        form.instance.username = username
        form.instance.set_password(f'1100@0011{username}0011@0011')
        form.instance.is_employee = True
        form.instance.is_staff = False

        return super().form_valid(form)

    def get_success_url(self):
        if SYS_VERIFICATION_EMAILS and not sent_email_over_employee_create(self.object):
            messages.warning(self.request, "Failed to sent email verification")

        return reverse_lazy('admins:user-list')


@method_decorator(admin_protected, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['profile_image', 'first_name', 'last_name', 'email', 'username', 'is_staff', 'is_employee', 'is_active']
    template_name = 'admins/user_form.html'
    success_url = reverse_lazy('admins:user-list')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        if self.object.is_employee:
            context['employee_form'] = EmployeeForm(instance=Employee.objects.filter(user=self.object).first())
            context['document_form'] = UserDocumentForm()
        return context


@method_decorator(admin_protected, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/client_confirm_delete.html'
    success_url = reverse_lazy('admins:user-list')


@method_decorator(admin_protected, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user_notes_form'] = EMPMGMTUserNotesForm(instance=self.object)
        if self.object.is_employee:
            employee = self.object.get_employee_profile()

            employee_sites_list = []
            employee_positions_list = []
            employee_department_list = []

            employee_id, created = EmployeeIdPass.objects.get_or_create(employee=employee)
            employee_work, created = EmployeeWork.objects.get_or_create(employee=employee)
            employee_health, created = EmployeeHealth.objects.get_or_create(employee=employee)
            employee_appearance, created = EmployeeAppearance.objects.get_or_create(employee=employee)

            context['sites'] = Site.objects.all()
            context['positions'] = Position.objects.all()
            context['departments'] = Department.objects.all()

            [employee_sites_list.append(x[0]) for x in employee.sites.all().values_list('pk')]
            [employee_department_list.append(x[0]) for x in employee.departments.all().values_list('pk')]
            [employee_positions_list.append(x[0]) for x in employee.positions.all().values_list('pk')]

            context['employee_sites_list'] = employee_sites_list
            context['employee_positions_list'] = employee_positions_list
            context['employee_department_list'] = employee_department_list

            context['employee'] = employee
            context['employee_id'] = employee_id
            context['employee_work'] = employee_work
            context['employee_health'] = employee_health
            context['employee_appearance'] = employee_appearance

            context['employee_form'] = EMPMGMTEmployeeForm(instance=employee)
            context['employee_id_form'] = EMPMGMTEmployeeIdPassForm(instance=employee_id)
            context['employee_work_form'] = EMPMGMTEmployeeWorkForm(instance=employee_work)
            context['employee_health_form'] = EMPMGMTEmployeeHealthForm(instance=employee_health)
            context['employee_appearance_form'] = EMPMGMTEmployeeAppearanceForm(instance=employee_appearance)

            context['employee_contracts'] = EmployeeContract.objects.filter(employee=employee)
            context['employee_docs'] = EmployeeDocument.objects.filter(employee=employee)
            context['employee_educations'] = EmployeeEducation.objects.filter(employee=employee)
            context['employee_employments'] = EmployeeEmployment.objects.filter(employee=employee)
            context['employee_qualifications'] = EmployeeQualification.objects.filter(employee=employee)
            context['employee_trainings'] = EmployeeTraining.objects.filter(employee=employee)
            context['employee_language_skills'] = EmployeeLanguageSkill.objects.filter(employee=employee)
            context['employee_emergency_contacts'] = EmployeeEmergencyContact.objects.filter(employee=employee)

            context['employee_contracts_form'] = EMPMGMTEmployeeContractForm()
            context['employee_docs_form'] = EMPMGMTEmployeeDocumentForm()
            context['employee_educations_form'] = EMPMGMTEmployeeEducationForm()
            context['employee_employments_form'] = EMPMGMTEmployeeEmploymentForm()
            context['employee_qualifications_form'] = EMPMGMTEmployeeQualificationForm()
            context['employee_trainings_form'] = EMPMGMTEmployeeTrainingForm()
            context['employee_language_skills_form'] = EMPMGMTEmployeeLanguageSkillForm()
            context['employee_emergency_contacts_form'] = EMPMGMTEmployeeEmergencyContactForm()
        return context


@method_decorator(admin_protected, name='dispatch')
class UserPasswordResetView(View):
    model = User
    template_name = 'admins/user_password_change.html'
    success_url = reverse_lazy('admins:user-list')
    context = {}

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/user_password_change.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
        return render(request, 'admins/user_password_change.html', {'form': form})


""" CLIENTS and CONTACTS """


@method_decorator(admin_protected, name='dispatch')
class ClientListView(ListView):
    queryset = Client.objects.all()
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        _filter = ClientFilter(self.request.GET, queryset=self.queryset)
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(admin_protected, name='dispatch')
class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(admin_protected, name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('admins:client-list')


@method_decorator(admin_protected, name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('admins:client-list')


@method_decorator(admin_protected, name='dispatch')
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('admins:client-list')


""" SITES """


@method_decorator(admin_protected, name='dispatch')
class SiteListView(ListView):
    queryset = Site.objects.all()
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        _filter = SiteFilter(self.request.GET, queryset=self.queryset)
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(admin_protected, name='dispatch')
class SiteDetailView(DetailView):
    model = Site

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(admin_protected, name='dispatch')
class SiteCreateView(CreateView):
    model = Site
    fields = '__all__'
    success_url = reverse_lazy('admins:site-list')


@method_decorator(admin_protected, name='dispatch')
class SiteUpdateView(UpdateView):
    model = Site
    fields = '__all__'
    success_url = reverse_lazy('admins:site-list')


@method_decorator(admin_protected, name='dispatch')
class SiteDeleteView(DeleteView):
    model = Site
    success_url = reverse_lazy('admins:site-list')


""" SHIFTS """


@method_decorator(admin_protected, name='dispatch')
class ShiftListView(ListView):
    model = Shift
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(ShiftListView, self).get_context_data(**kwargs)
        filter_object = ShiftFilter(self.request.GET, queryset=Shift.objects.all())
        context['filter_form'] = filter_object.form

        paginator = Paginator(filter_object.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


@method_decorator(admin_protected, name='dispatch')
class ShiftDetailView(DetailView):
    model = Shift

    def get_context_data(self, **kwargs):
        context = super(ShiftDetailView, self).get_context_data(**kwargs)
        context['current_date'] = datetime.date.today()
        return context


@method_decorator(admin_protected, name='dispatch')
class ShiftCreateView(CreateView):
    model = Shift
    fields = '__all__'

    def form_valid(self, form):
        return super(ShiftCreateView, self).form_valid(form)

    def get_success_url(self):
        shifts_create_update(self.object, self.request.POST)
        return reverse_lazy('admins:shift-detail', args=[self.object.pk])


class ShiftCustomCreateView(View):
    template_name = "admins/shift_custom_create_form.html"

    def get(self, request, *args, **kwargs):
        context = {
            'employees': Employee.objects.all(),
            'positions': Position.objects.all(),
            'clients': Client.objects.all()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass


@method_decorator(admin_protected, name='dispatch')
class ShiftUpdateView(UpdateView):
    model = Shift
    fields = [
        'start_date', 'end_date', 'start_time', 'end_time', 'site', 'position', 'employee',
        'pay_rate', 'charge_rate', 'extra_charges', 'repeat_policy'
    ]
    previous_shift = None

    def dispatch(self, request, *args, **kwargs):
        self.previous_shift = get_object_or_404(Shift, pk=kwargs['pk'])
        return super(ShiftUpdateView, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(ShiftUpdateView, self).get_context_data(**kwargs)
        week_list = self.object.get_week_shifts_status()

        if self.object.repeat_policy == 'w':
            context['monday'] = 'checked' if week_list[0] else ''
            context['tuesday'] = 'checked' if week_list[1] else ''
            context['wednesday'] = 'checked' if week_list[2] else ''
            context['thursday'] = 'checked' if week_list[3] else ''
            context['friday'] = 'checked' if week_list[4] else ''
            context['saturday'] = 'checked' if week_list[5] else ''
            context['sunday'] = 'checked' if week_list[6] else ''

        return context

    def get_success_url(self):
        shifts_create_update(self.object, self.request.POST, False, False, self.previous_shift)
        return reverse_lazy('admins:shift-detail', args=[self.object.pk])


@method_decorator(admin_protected, name='dispatch')
class ShiftDeleteView(DeleteView):
    model = Shift
    success_url = reverse_lazy('admins:shift-list')


""" SHIFT DAY """


@method_decorator(admin_protected, name='dispatch')
class ShiftDayUpdateView(UpdateView):
    model = ShiftDay
    fields = [
        'employee', 'clock_in', 'clock_out'
    ]

    def get_success_url(self):
        return reverse_lazy('admins:shift-detail', args=[self.object.shift.pk])


@method_decorator(admin_protected, name='dispatch')
class ShiftDayDeleteView(DeleteView):
    model = ShiftDay
    success_url = reverse_lazy('admins:shift-list')

    def get_success_url(self):
        return reverse_lazy("admins:shift-detail", args=[self.object.shift.pk])


""" ReportTypeS """


@method_decorator(admin_protected, name='dispatch')
class ReportTypeListView(ListView):
    queryset = ReportType.objects.all()


@method_decorator(admin_protected, name='dispatch')
class ReportTypeCreateView(CreateView):
    model = ReportType
    fields = '__all__'
    success_url = reverse_lazy('admins:report-type-list')


@method_decorator(admin_protected, name='dispatch')
class ReportTypeUpdateView(UpdateView):
    model = ReportType
    fields = '__all__'
    success_url = reverse_lazy('admins:report-type-list')


@method_decorator(admin_protected, name='dispatch')
class ReportTypeDeleteView(DeleteView):
    model = ReportType
    success_url = reverse_lazy('admins:report-type-list')


""" Absense Types """


@method_decorator(admin_protected, name='dispatch')
class AbsenseTypeListView(ListView):
    queryset = AbsenseType.objects.all()


@method_decorator(admin_protected, name='dispatch')
class AbsenseTypeCreateView(CreateView):
    model = AbsenseType
    fields = '__all__'
    success_url = reverse_lazy('admins:absense-type-list')


@method_decorator(admin_protected, name='dispatch')
class AbsenseTypeUpdateView(UpdateView):
    model = AbsenseType
    fields = '__all__'
    success_url = reverse_lazy('admins:absense-type-list')


@method_decorator(admin_protected, name='dispatch')
class AbsenseTypeDeleteView(DeleteView):
    model = AbsenseType
    success_url = reverse_lazy('admins:absense-type-list')


""" Sub Contractors """


@method_decorator(admin_protected, name='dispatch')
class SubContractorListView(ListView):
    queryset = SubContractor.objects.all()
    template_name = 'admins/subcontractor_list.html'


@method_decorator(admin_protected, name='dispatch')
class SubContractorCreateView(CreateView):
    model = SubContractor
    form_class = SubContractorForm
    template_name = 'admins/subcontractor_form.html'
    success_url = reverse_lazy('admins:sub-contractor-list')


@method_decorator(admin_protected, name='dispatch')
class SubContractorUpdateView(UpdateView):
    model = SubContractor
    form_class = SubContractorForm
    template_name = 'admins/subcontractor_form.html'
    success_url = reverse_lazy('admins:sub-contractor-list')


@method_decorator(admin_protected, name='dispatch')
class SubContractorDetailView(DetailView):
    model = SubContractor
    template_name = 'admins/subcontractor_detail.html'


@method_decorator(admin_protected, name='dispatch')
class SubContractorDeleteView(DeleteView):
    model = SubContractor
    template_name = 'admins/subcontractor_confirm_delete.html'
    success_url = reverse_lazy('admins:sub-contractor-list')


