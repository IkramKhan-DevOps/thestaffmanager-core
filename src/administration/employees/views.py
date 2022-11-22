import datetime

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, UpdateView

from src.accounts.decorators import employee_protected
from src.administration.admins.models import Shift


@method_decorator(employee_protected, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'employees/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['shifts'] = Shift.objects.filter(employee__user=self.request.user)
        return context


@method_decorator(employee_protected, name='dispatch')
class ShiftListView(ListView):
    template_name = 'employees/shift_list.html'

    def get_queryset(self):
        return Shift.objects.filter(employee__user=self.request.user)


@method_decorator(employee_protected, name='dispatch')
class ShiftDetailView(DetailView):
    model = Shift
    template_name = 'employees/shift_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShiftDetailView, self).get_context_data(**kwargs)
        context['current_date'] = datetime.date.today()
        return context
