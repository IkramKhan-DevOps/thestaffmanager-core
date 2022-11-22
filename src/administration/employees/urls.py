from django.urls import path
from .views import (
    DashboardView, ShiftListView, ShiftDetailView
)

app_name = 'employees'
urlpatterns = [

    path('', DashboardView.as_view(), name="dashboard"),
    path('my/shift/', ShiftListView.as_view(), name="shift-list"),
    path('my/shift/<int:pk>/', ShiftDetailView.as_view(), name="shift-detail"),

]
