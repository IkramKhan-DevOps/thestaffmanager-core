from django.urls import path
from .views import (
    CountryJsonView,
    EmployeeJsonView, EmployeeWorkJsonView, EmployeeHealthJsonView, EmployeeAppearanceJsonView,
    EmployeeContractGenericJsonView
)

app_name = 'admins-json'
urlpatterns = [

    path('country/add/', CountryJsonView.as_view(), name='country_add'),
    path('country/<int:pk>/change/', CountryJsonView.as_view(), name='country_change'),
    path('country/<int:pk>/delete/', CountryJsonView.as_view(), name='country_delete'),

    path('employee/<int:pk>/change/', EmployeeJsonView.as_view(), name="employee_change"),
    path('employee/<int:pk>/work/change/', EmployeeWorkJsonView.as_view(), name="employee_work_change"),
    path('employee/<int:pk>/health/change/', EmployeeHealthJsonView.as_view(), name="employee_health_change"),
    path(
        'employee/<int:pk>/appearance/change/', EmployeeAppearanceJsonView.as_view(), name="employee_appearance_change"
    ),

    path(
        'employee/contract/add/', EmployeeContractGenericJsonView.as_view(),
        name="employee_contract_add"
    ),
    path(
        'employee/contract/<int:pk>/delete/', EmployeeContractGenericJsonView.as_view(),
        name="employee_contract_delete"
    ),

]
