import datetime

from django.views.generic import TemplateView, ListView, DetailView, UpdateView

from src.administration.admins.models import Shift


class DashboardView(TemplateView):
    template_name = 'employees/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['shifts'] = Shift.objects.filter(employee__user=self.request.user)
        return context


class ShiftListView(ListView):
    template_name = 'employees/shift_list.html'

    def get_queryset(self):
        return Shift.objects.filter(employee__user=self.request.user)


class ShiftDetailView(DetailView):
    model = Shift
    template_name = 'employees/shift_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShiftDetailView, self).get_context_data(**kwargs)
        context['current_date'] = datetime.date.today()
        return context
