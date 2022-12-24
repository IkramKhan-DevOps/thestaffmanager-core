from django.urls import path
from .views import (
    CountryJsonView,
    EmployeeJsonView, EmployeeWorkJsonView, EmployeeHealthJsonView, EmployeeAppearanceJsonView,
    EmployeeContractGenericJsonView, EmployeeQualificationAddJsonView, EmployeeQualificationDeleteJsonView,
    EmployeeTrainingAddJsonView, EmployeeTrainingDeleteJsonView, EmployeeLanguageSkillAddJsonView,
    EmployeeLanguageSkillDeleteJsonView
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

    path('employee/contract/add/', EmployeeContractGenericJsonView.as_view(),name="employee_contract_add"),
    path('employee/contract/<int:pk>/delete/', EmployeeContractGenericJsonView.as_view(),name="employee_contract_delete"),

    path('employee/qualification/add/', EmployeeQualificationAddJsonView.as_view(), name='employee_qualification_add'),
    path('employee/qualification/<int:pk>/delete/', EmployeeQualificationDeleteJsonView.as_view(), name='employee_qualification_delete'),
    path('employee/training/add/', EmployeeTrainingAddJsonView.as_view(), name='employee_training_add'),
    path('employee/training/<int:pk>/delete/', EmployeeTrainingDeleteJsonView.as_view(), name='employee_training_delete'),
    path('employee/language/add/', EmployeeLanguageSkillAddJsonView.as_view(), name='employee_language_add'),
    path('employee/language/<int:pk>/delete/', EmployeeLanguageSkillDeleteJsonView.as_view(),name='employee_language_delete'),

]
