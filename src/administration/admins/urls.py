from django.urls import path, include
from .views import (
    DashboardView,
    PositionListView, PositionDeleteView, PositionCreateView, PositionUpdateView, PositionDetailView,
    UserPasswordResetView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView,
    SiteListView, SiteDetailView, SiteUpdateView, SiteDeleteView, SiteCreateView,
    ReportTypeListView, ReportTypeDetailView, ReportTypeUpdateView, ReportTypeDeleteView, ReportTypeCreateView,

    AuditLogView, LiveChatView, CasesView, CallsView, PipelineView,
    ScheduleView, ShiftsView, TimeClockView, AbsencesView,
    PayRunReportView, ShiftNotesView, ChargesBreakView, ReportsView, HealthView, ShiftListView, ShiftDetailView,
    ShiftCreateView, ShiftUpdateView, ShiftDeleteView
)

app_name = 'admins'
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('live-chat/', LiveChatView.as_view(), name="live-chat"),

    path('schedule/', ScheduleView.as_view(), name="schedule"),
    path('shifts/', ShiftsView.as_view(), name="shifts"),
    path('time-clock/', TimeClockView.as_view(), name="time-clock"),
    path('absences/', AbsencesView.as_view(), name="absences"),

    path('cases/', CasesView.as_view(), name="cases"),
    path('pipelines/', PipelineView.as_view(), name="pipeline"),
    path('calls/', CallsView.as_view(), name="calls"),

    path('reports/', ReportsView.as_view(), name="reports"),
    path('shift-notes/', ShiftNotesView.as_view(), name="shift-notes"),
    path('charges-break/', ChargesBreakView.as_view(), name="charges-break"),
    path('pay-run-report/', PayRunReportView.as_view(), name="pay-run-report"),
    path('health/', HealthView.as_view(), name="health"),

    path('audit-log/', AuditLogView.as_view(), name="audit-log"),
]

urlpatterns += [
    path('position/', PositionListView.as_view(), name='position-list'),
    path('position/add/', PositionCreateView.as_view(), name='position-add'),
    path('position/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
    path('position/<int:pk>/change/', PositionUpdateView.as_view(), name='position-update'),
    path('position/<int:pk>/delete/', PositionDeleteView.as_view(), name='position-delete'),
]

urlpatterns += [
    path('shift/', ShiftListView.as_view(), name='shift-list'),
    path('shift/add/', ShiftCreateView.as_view(), name='shift-add'),
    path('shift/<int:pk>/', ShiftDetailView.as_view(), name='shift-detail'),
    path('shift/<int:pk>/change/', ShiftUpdateView.as_view(), name='shift-update'),
    path('shift/<int:pk>/delete/', ShiftDeleteView.as_view(), name='shift-delete'),
]

urlpatterns += [
    path('client/', ClientListView.as_view(), name='client-list'),
    path('client/add/', ClientCreateView.as_view(), name='client-add'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:pk>/change/', ClientUpdateView.as_view(), name='client-update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
]

urlpatterns += [
    path('site/', SiteListView.as_view(), name='site-list'),
    path('site/add/', SiteCreateView.as_view(), name='site-add'),
    path('site/<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
    path('site/<int:pk>/change/', SiteUpdateView.as_view(), name='site-update'),
    path('site/<int:pk>/delete/', SiteDeleteView.as_view(), name='site-delete'),
]

urlpatterns += [
    path('report-type/', ReportTypeListView.as_view(), name='report-type-list'),
    path('report-type/add/', ReportTypeCreateView.as_view(), name='report-type-add'),
    path('report-type/<int:pk>/', ReportTypeDetailView.as_view(), name='report-type-detail'),
    path('report-type/<int:pk>/change/', ReportTypeUpdateView.as_view(), name='report-type-update'),
    path('report-type/<int:pk>/delete/', ReportTypeDeleteView.as_view(), name='report-type-delete'),
]

urlpatterns += [
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/add/', UserCreateView.as_view(), name='user-add'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user/<int:pk>/reset/password/', UserPasswordResetView.as_view(), name='user-password-reset'),
]

urlpatterns += [
    path('api/', include('src.administration.admins.admins-api.urls', namespace='admins-api'))
]