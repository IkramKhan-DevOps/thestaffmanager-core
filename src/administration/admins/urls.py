from django.urls import path
from .views import (
    DashboardView,
    PositionListView, PositionDeleteView, PositionCreateView, PositionUpdateView, PositionDetailView,
    UserPasswordResetView, EmployeeMapView, PostCodeReportView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView,
    ContactListView, ContactDetailView, ContactUpdateView, ContactDeleteView, ContactCreateView,
    SiteListView, SiteDetailView, SiteUpdateView, SiteDeleteView, SiteCreateView,
    AssetListView, AssetDetailView, AssetUpdateView, AssetDeleteView, AssetCreateView,
    QualificationListView, QualificationDetailView, QualificationUpdateView, QualificationDeleteView,
    QualificationCreateView,
    VehicleListView, VehicleDetailView, VehicleUpdateView, VehicleDeleteView, VehicleCreateView,
    ReportTypeListView, ReportTypeDetailView, ReportTypeUpdateView, ReportTypeDeleteView, ReportTypeCreateView,
    AssetAuditListView, AssetAuditDetailView, AssetAuditUpdateView, AssetAuditDeleteView, AssetAuditCreateView,
    EmailAccountListView, EmailAccountDetailView, EmailAccountUpdateView, EmailAccountDeleteView,
    EmailAccountCreateView,
    FormBuilderListView, FormBuilderDetailView, FormBuilderUpdateView, FormBuilderDeleteView, FormBuilderCreateView,

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

    path('employee-map/', EmployeeMapView.as_view(), name="employee-map"),

    path('post-code-report/', PostCodeReportView.as_view(), name="post-code-report"),
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
    path('contact/', ContactListView.as_view(), name='contact-list'),
    path('contact/add/', ContactCreateView.as_view(), name='contact-add'),
    path('contact/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('contact/<int:pk>/change/', ContactUpdateView.as_view(), name='contact-update'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact-delete'),
]

urlpatterns += [
    path('site/', SiteListView.as_view(), name='site-list'),
    path('site/add/', SiteCreateView.as_view(), name='site-add'),
    path('site/<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
    path('site/<int:pk>/change/', SiteUpdateView.as_view(), name='site-update'),
    path('site/<int:pk>/delete/', SiteDeleteView.as_view(), name='site-delete'),
]

urlpatterns += [
    path('asset/', AssetListView.as_view(), name='asset-list'),
    path('asset/add/', AssetCreateView.as_view(), name='asset-add'),
    path('asset/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('asset/<int:pk>/change/', AssetUpdateView.as_view(), name='asset-update'),
    path('asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='asset-delete'),
]

urlpatterns += [
    path('vehicle/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle/add/', VehicleCreateView.as_view(), name='vehicle-add'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicle/<int:pk>/change/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),
]

urlpatterns += [
    path('qualification/', QualificationListView.as_view(), name='qualification-list'),
    path('qualification/add/', QualificationCreateView.as_view(), name='qualification-add'),
    path('qualification/<int:pk>/', QualificationDetailView.as_view(), name='qualification-detail'),
    path('qualification/<int:pk>/change/', QualificationUpdateView.as_view(), name='qualification-update'),
    path('qualification/<int:pk>/delete/', QualificationDeleteView.as_view(), name='qualification-delete'),
]

urlpatterns += [
    path('report-type/', ReportTypeListView.as_view(), name='report-type-list'),
    path('report-type/add/', ReportTypeCreateView.as_view(), name='report-type-add'),
    path('report-type/<int:pk>/', ReportTypeDetailView.as_view(), name='report-type-detail'),
    path('report-type/<int:pk>/change/', ReportTypeUpdateView.as_view(), name='report-type-update'),
    path('report-type/<int:pk>/delete/', ReportTypeDeleteView.as_view(), name='report-type-delete'),
]

urlpatterns += [
    path('email-account/', EmailAccountListView.as_view(), name='email-account-list'),
    path('email-account/add/', EmailAccountCreateView.as_view(), name='email-account-add'),
    path('email-account/<int:pk>/', EmailAccountDetailView.as_view(), name='email-account-detail'),
    path('email-account/<int:pk>/change/', EmailAccountUpdateView.as_view(), name='email-account-update'),
    path('email-account/<int:pk>/delete/', EmailAccountDeleteView.as_view(), name='email-account-delete'),
]

urlpatterns += [
    path('form-builder/', FormBuilderListView.as_view(), name='form-builder-list'),
    path('form-builder/add/', FormBuilderCreateView.as_view(), name='form-builder-add'),
    path('form-builder/<int:pk>/', FormBuilderDetailView.as_view(), name='form-builder-detail'),
    path('form-builder/<int:pk>/change/', FormBuilderUpdateView.as_view(), name='form-builder-update'),
    path('form-builder/<int:pk>/delete/', FormBuilderDeleteView.as_view(), name='form-builder-delete'),
]

urlpatterns += [
    path('asset-audit/', AssetAuditListView.as_view(), name='asset-audit-list'),
    path('asset-audit/add/', AssetAuditCreateView.as_view(), name='asset-audit-add'),
    path('asset-audit/<int:pk>/', AssetAuditDetailView.as_view(), name='asset-audit-detail'),
    path('asset-audit/<int:pk>/change/', AssetAuditUpdateView.as_view(), name='asset-audit-update'),
    path('asset-audit/<int:pk>/delete/', AssetAuditDeleteView.as_view(), name='asset-audit-delete'),
]

urlpatterns += [
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/add/', UserCreateView.as_view(), name='user-add'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user/<int:pk>/reset/password/', UserPasswordResetView.as_view(), name='user-password-reset'),
]
