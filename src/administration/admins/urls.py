from django.urls import path, include
from .views import (
    DashboardView, ScheduleView, TimeClockView,
    PositionListView, PositionDeleteView, PositionCreateView, PositionUpdateView,
    UserPasswordResetView, UserListView, UserStaffCreateView, UserEmployeeCreateView, UserUpdateView, UserDeleteView,
    ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView,
    SiteListView, SiteDetailView, SiteUpdateView, SiteDeleteView, SiteCreateView,
    ReportTypeListView, ReportTypeUpdateView, ReportTypeDeleteView, ReportTypeCreateView,
    ShiftDayUpdateView, ShiftDayDeleteView,
    ShiftCreateView, ShiftUpdateView, ShiftDeleteView, UserDetailView,
    ShiftListView, ShiftDetailView, ShiftCustomCreateView,
    CountryListView, CountryCreateView, CountryUpdateView, CountryDeleteView, SubContractorListView,
    SubContractorCreateView, SubContractorUpdateView, SubContractorDeleteView, SubContractorDetailView,
    DepartmentListView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView
)

app_name = 'admins'
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('schedule/', ScheduleView.as_view(), name="schedule"),
    path('time-clock/', TimeClockView.as_view(), name="time-clock"),
]

urlpatterns += [
    path('position/', PositionListView.as_view(), name='position-list'),
    path('position/add/', PositionCreateView.as_view(), name='position-add'),
    path('position/<int:pk>/change/', PositionUpdateView.as_view(), name='position-update'),
    path('position/<int:pk>/delete/', PositionDeleteView.as_view(), name='position-delete'),
]

urlpatterns += [
    path('country/', CountryListView.as_view(), name='country-list'),
    path('country/add/', CountryCreateView.as_view(), name='country-add'),
    path('country/<int:pk>/change/', CountryUpdateView.as_view(), name='country-update'),
    path('country/<int:pk>/delete/', CountryDeleteView.as_view(), name='country-delete'),
]

urlpatterns += [
    path('department/', DepartmentListView.as_view(), name='department-list'),
    path('department/add/', DepartmentCreateView.as_view(), name='department-add'),
    path('department/<int:pk>/change/', DepartmentUpdateView.as_view(), name='department-update'),
    path('department/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department-delete'),
]

urlpatterns += [
    path('shift/', ShiftListView.as_view(), name='shift-list'),
    path('shift/add/', ShiftCreateView.as_view(), name='shift-add'),
    path('shift/<int:pk>/', ShiftDetailView.as_view(), name='shift-detail'),
    path('shift/<int:pk>/change/', ShiftUpdateView.as_view(), name='shift-update'),
    path('shift/<int:pk>/delete/', ShiftDeleteView.as_view(), name='shift-delete'),
]

urlpatterns += [
    path('shift-day/<int:pk>/change/', ShiftDayUpdateView.as_view(), name='shift-day-update'),
    path('shift-day/<int:pk>/delete/', ShiftDayDeleteView.as_view(), name='shift-day-delete'),
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
    path('report-type/<int:pk>/change/', ReportTypeUpdateView.as_view(), name='report-type-update'),
    path('report-type/<int:pk>/delete/', ReportTypeDeleteView.as_view(), name='report-type-delete'),
]

urlpatterns += [
    path('sub-contractor/', SubContractorListView.as_view(), name='sub-contractor-list'),
    path('sub-contractor/add/', SubContractorCreateView.as_view(), name='sub-contractor-add'),
    path('sub-contractor/<int:pk>/', SubContractorDetailView.as_view(), name='sub-contractor-detail'),
    path('sub-contractor/<int:pk>/change/', SubContractorUpdateView.as_view(), name='sub-contractor-update'),
    path('sub-contractor/<int:pk>/delete/', SubContractorDeleteView.as_view(), name='sub-contractor-delete'),
]

urlpatterns += [
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user/staff/add/', UserStaffCreateView.as_view(), name='user-staff-add'),
    path('user/employee/add/', UserEmployeeCreateView.as_view(), name='user-employee-add'),
    path('user/<int:pk>/reset/password/', UserPasswordResetView.as_view(), name='user-password-reset'),
]

urlpatterns += [
    path('api/', include('src.administration.admins.admins-api.urls', namespace='admins-api')),
    path('json/', include('src.administration.admins.admins-json.urls', namespace='admins-json'))
]
