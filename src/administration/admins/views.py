from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AdminPasswordChangeForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, DeleteView,
    CreateView)

from .models import (
    Position, Client, Contact, Site, Asset, Qualification, Vehicle, ReportType,
    EmailAccount, FormBuilder, AssetAudit, Shift, ShiftDay,
)
import calendar
import datetime

""" MAIN """


def date_range(start, end):
    """
    :param start:
    :param end:
    :return dates in range:

    :desc check this first if it is in month, year and daily routine vise
    """
    delta = end - start

    # TODO:REQUIREMENT: add checks here month repeat - weekly repeat
    days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    return days


def shifts_create_update_logic(shift, is_create=True):
    """
    :param shift:
    :param is_create:
    :return None:

    ":desc add new one's and delete previous ones"

    """

    dates = date_range(shift.start_date, shift.end_date)

    # TODO:ALERT: this deletes all previous records and adds new ones --
    #  this logic is wrong if data is long and lengthy
    if not is_create:
        ShiftDay.objects.filter(shift=shift).delete()
        [ShiftDay.objects.create(shift_date=_date, shift=shift) for _date in dates]


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/news-feed.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class PositionListView(ListView):
    queryset = Position.objects.all()


@method_decorator(login_required, name='dispatch')
class PositionDetailView(DetailView):
    model = Position

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class PositionCreateView(CreateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('admins:position-list')


@method_decorator(login_required, name='dispatch')
class PositionUpdateView(UpdateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('admins:position-list')


@method_decorator(login_required, name='dispatch')
class PositionDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy('admins:position-list')


""" STUDENT CLASS """


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.all()
    template_name = 'admins/user_list.html'


@method_decorator(login_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'admins/user_form.html'
    success_url = reverse_lazy('admins:user-list')

    def form_valid(self, form):
        form.instance.is_staff = True
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active']
    template_name = 'admins/user_form.html'
    success_url = reverse_lazy('admins:user-list')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['update'] = True
        return context


@method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/client_confirm_delete.html'
    success_url = reverse_lazy('admins:user-list')


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ClientListView(ListView):
    queryset = Client.objects.all()


@method_decorator(login_required, name='dispatch')
class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('admins:client-list')


@method_decorator(login_required, name='dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('admins:client-list')


@method_decorator(login_required, name='dispatch')
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('admins:client-list')


""" CONTACTS """


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    queryset = Contact.objects.all()


@method_decorator(login_required, name='dispatch')
class ContactDetailView(DetailView):
    model = Contact

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    model = Contact
    fields = '__all__'
    success_url = reverse_lazy('admins:contact-list')


@method_decorator(login_required, name='dispatch')
class ContactUpdateView(UpdateView):
    model = Contact
    fields = '__all__'
    success_url = reverse_lazy('admins:contact-list')


@method_decorator(login_required, name='dispatch')
class ContactDeleteView(DeleteView):
    model = Contact
    success_url = reverse_lazy('admins:contact-list')


""" SITES """


@method_decorator(login_required, name='dispatch')
class SiteListView(ListView):
    queryset = Site.objects.all()


@method_decorator(login_required, name='dispatch')
class SiteDetailView(DetailView):
    model = Site

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class SiteCreateView(CreateView):
    model = Site
    fields = '__all__'
    success_url = reverse_lazy('admins:site-list')


@method_decorator(login_required, name='dispatch')
class SiteUpdateView(UpdateView):
    model = Site
    fields = '__all__'
    success_url = reverse_lazy('admins:site-list')


@method_decorator(login_required, name='dispatch')
class SiteDeleteView(DeleteView):
    model = Site
    success_url = reverse_lazy('admins:site-list')


@method_decorator(login_required, name='dispatch')
class ShiftListView(ListView):
    model = Shift


@method_decorator(login_required, name='dispatch')
class ShiftDetailView(DetailView):
    model = Shift

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShiftDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ShiftCreateView(CreateView):
    model = Shift
    fields = '__all__'

    def get_success_url(self):
        shifts_create_update_logic(self.object, is_create=True)
        return reverse_lazy('admins:shift-list')


@method_decorator(login_required, name='dispatch')
class ShiftUpdateView(UpdateView):
    model = Shift
    fields = '__all__'

    def get_success_url(self):
        shifts_create_update_logic(self.object, is_create=False)
        return reverse_lazy('admins:shift-list')


@method_decorator(login_required, name='dispatch')
class ShiftDeleteView(DeleteView):
    model = Shift
    success_url = reverse_lazy('admins:shift-list')


""" ASSETS """


@method_decorator(login_required, name='dispatch')
class AssetListView(ListView):
    queryset = Asset.objects.all()


@method_decorator(login_required, name='dispatch')
class AssetDetailView(DetailView):
    model = Asset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssetDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class AssetCreateView(CreateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('admins:asset-list')


@method_decorator(login_required, name='dispatch')
class AssetUpdateView(UpdateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('admins:asset-list')


@method_decorator(login_required, name='dispatch')
class AssetDeleteView(DeleteView):
    model = Asset
    success_url = reverse_lazy('admins:asset-list')


""" QualificationS """


@method_decorator(login_required, name='dispatch')
class QualificationListView(ListView):
    queryset = Qualification.objects.all()


@method_decorator(login_required, name='dispatch')
class QualificationDetailView(DetailView):
    model = Qualification

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QualificationDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class QualificationCreateView(CreateView):
    model = Qualification
    fields = '__all__'
    success_url = reverse_lazy('admins:qualification-list')


@method_decorator(login_required, name='dispatch')
class QualificationUpdateView(UpdateView):
    model = Qualification
    fields = '__all__'
    success_url = reverse_lazy('admins:qualification-list')


@method_decorator(login_required, name='dispatch')
class QualificationDeleteView(DeleteView):
    model = Qualification
    success_url = reverse_lazy('admins:qualification-list')


""" VehicleS """


@method_decorator(login_required, name='dispatch')
class VehicleListView(ListView):
    queryset = Vehicle.objects.all()


@method_decorator(login_required, name='dispatch')
class VehicleDetailView(DetailView):
    model = Vehicle

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VehicleDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class VehicleCreateView(CreateView):
    model = Vehicle
    fields = '__all__'
    success_url = reverse_lazy('admins:vehicle-list')


@method_decorator(login_required, name='dispatch')
class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = '__all__'
    success_url = reverse_lazy('admins:vehicle-list')


@method_decorator(login_required, name='dispatch')
class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('admins:vehicle-list')


""" ReportTypeS """


@method_decorator(login_required, name='dispatch')
class ReportTypeListView(ListView):
    queryset = ReportType.objects.all()


@method_decorator(login_required, name='dispatch')
class ReportTypeDetailView(DetailView):
    model = ReportType

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReportTypeDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ReportTypeCreateView(CreateView):
    model = ReportType
    fields = '__all__'
    success_url = reverse_lazy('admins:report-type-list')


@method_decorator(login_required, name='dispatch')
class ReportTypeUpdateView(UpdateView):
    model = ReportType
    fields = '__all__'
    success_url = reverse_lazy('admins:report-type-list')


@method_decorator(login_required, name='dispatch')
class ReportTypeDeleteView(DeleteView):
    model = ReportType
    success_url = reverse_lazy('admins:report-type-list')


""" AssetAuditS """


@method_decorator(login_required, name='dispatch')
class AssetAuditListView(ListView):
    queryset = AssetAudit.objects.all()


@method_decorator(login_required, name='dispatch')
class AssetAuditDetailView(DetailView):
    model = AssetAudit

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssetAuditDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class AssetAuditCreateView(CreateView):
    model = AssetAudit
    fields = '__all__'
    success_url = reverse_lazy('admins:asset-audit-list')


@method_decorator(login_required, name='dispatch')
class AssetAuditUpdateView(UpdateView):
    model = AssetAudit
    fields = '__all__'
    success_url = reverse_lazy('admins:asset-audit-list')


@method_decorator(login_required, name='dispatch')
class AssetAuditDeleteView(DeleteView):
    model = AssetAudit
    success_url = reverse_lazy('admins:asset-audit-list')


""" FormBuilderS """


@method_decorator(login_required, name='dispatch')
class FormBuilderListView(ListView):
    queryset = FormBuilder.objects.all()


@method_decorator(login_required, name='dispatch')
class FormBuilderDetailView(DetailView):
    model = FormBuilder

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FormBuilderDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class FormBuilderCreateView(CreateView):
    model = FormBuilder
    fields = '__all__'
    success_url = reverse_lazy('admins:form-builder-list')


@method_decorator(login_required, name='dispatch')
class FormBuilderUpdateView(UpdateView):
    model = FormBuilder
    fields = '__all__'
    success_url = reverse_lazy('admins:form-builder-list')


@method_decorator(login_required, name='dispatch')
class FormBuilderDeleteView(DeleteView):
    model = FormBuilder
    success_url = reverse_lazy('admins:form-builder-list')


""" EmailAccountS """


@method_decorator(login_required, name='dispatch')
class EmailAccountListView(ListView):
    queryset = EmailAccount.objects.all()


@method_decorator(login_required, name='dispatch')
class EmailAccountDetailView(DetailView):
    model = EmailAccount

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmailAccountDetailView, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class EmailAccountCreateView(CreateView):
    model = EmailAccount
    fields = '__all__'
    success_url = reverse_lazy('admins:email-account-list')


@method_decorator(login_required, name='dispatch')
class EmailAccountUpdateView(UpdateView):
    model = EmailAccount
    fields = '__all__'
    success_url = reverse_lazy('admins:email-account-list')


@method_decorator(login_required, name='dispatch')
class EmailAccountDeleteView(DeleteView):
    model = EmailAccount
    success_url = reverse_lazy('admins:email-account-list')


""" OTHER """


@method_decorator(login_required, name='dispatch')
class EmployeeMapView(TemplateView):
    template_name = 'admins/employee_map.html'


@method_decorator(login_required, name='dispatch')
class PostCodeReportView(TemplateView):
    template_name = 'admins/post_code_report.html'


""" --------------------------------------------- """


@method_decorator(login_required, name='dispatch')
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
                'id', 'shift_id', 'shift__start_time', 'shift__end_time', 'shift__client__name', 'shift_date'
            )

            # CHECK1: if request contains date in get
            requested_month = _request.GET.get('month')
            requested_year = _request.GET.get('year')

            if (requested_month and 0 < int(requested_month) < 13) and \
                    (requested_year and int(requested_year) > 0):

                print("validated")
                shifts_queryset = ShiftDay.objects.filter(
                    Q(shift_date__month=datetime.date.today().month,
                      shift_date__year=datetime.date.today().year)
                ).values(
                    'id', 'shift_id', 'shift__start_time', 'shift__end_time',
                    'shift__client__name', 'shift_date'
                )
                _current_year = requested_year
                _current_month = requested_month if int(requested_month) > 9 else "0" + requested_month

            return shifts_queryset, _current_month, _current_year

        # CALL: get month, year and query over it
        shifts, current_month, current_year = get_query_over_request(self.request)

        # DISPLAY: results
        print(current_month)
        print(current_year)

        # CONTEXT: data
        context['shifts'] = shifts
        context['current_day'] = "01"
        context['current_month'] = current_month
        context['current_year'] = current_year
        return context


@method_decorator(login_required, name='dispatch')
class ShiftsView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class TimeClockView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class AbsencesView(TemplateView):
    template_name = 'admins/construction.html'


""" --------------------------------------------- """


@method_decorator(login_required, name='dispatch')
class AuditLogView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class LiveChatView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class CasesView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class CallsView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class PipelineView(TemplateView):
    template_name = 'admins/construction.html'


""" --------------------------------------------- """


@method_decorator(login_required, name='dispatch')
class ReportsView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class ShiftNotesView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class ChargesBreakView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class PayRunReportView(TemplateView):
    template_name = 'admins/construction.html'


@method_decorator(login_required, name='dispatch')
class HealthView(TemplateView):
    template_name = 'admins/construction.html'
