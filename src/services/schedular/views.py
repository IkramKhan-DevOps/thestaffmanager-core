import datetime
from calendar import monthrange

from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from src.accounts.models import Employee
from src.administration.admins.forms import ShiftForm
from src.administration.admins.models import ShiftDay
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view

from src.accounts.decorators import admin_protected
from src.services.schedular.forms import ShiftModelForm

""" SCHEDULAR """


@method_decorator([admin_protected, never_cache], name='dispatch')
class ScheduleView(TemplateView):
    template_name = 'schedular/schedular.html'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)

        def get_query_over_request(_request):
            # DEFAULT: query year and month
            _current_month = datetime.date.today().month
            _current_year = datetime.date.today().year
            shifts_queryset = ShiftDay.objects.filter(
                Q(shift_date__month=datetime.date.today().month, shift_date__year=datetime.date.today().year)
            ).values(
                'id', 'shift_id', 'shift_date', 'shift_end_date',
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
        context['form'] = ShiftForm()
        context['employees'] = employees
        context['current_day'] = datetime.date.today().day
        context['current_month'] = current_month
        context['current_year'] = current_year
        context['current_date'] = datetime.date.today()

        # CONTEXT: month and days
        current_month_start_date = datetime.date(int(current_year), int(current_month), 1)
        total_days_in_this_month = monthrange(int(current_year), int(current_month))[1]
        current_month_end_date = datetime.date(int(current_year), int(current_month), total_days_in_this_month)
        context['current_month_start_date'] = current_month_start_date
        context['current_month_end_date'] = current_month_end_date

        return context


""" SHIFTS """


@method_decorator([admin_protected, json_view, csrf_exempt], name='dispatch')
class ShiftAddModelView(View):

    def post(self, request):
        form = ShiftModelForm(request.POST)
        if not form.is_valid():
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html}

        form.save(commit=True)
        return {'success': True}
