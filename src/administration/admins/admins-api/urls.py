from django.urls import path
from .views import ChangeTimesAPI, ShiftListAPIView, ShiftDayStatusChange

app_name = 'admins-api'
urlpatterns = [
    path('shift/<int:pk>/times/change/', ChangeTimesAPI.as_view(), name="shift-times-change"),
    path('shifts/', ShiftListAPIView.as_view(), name="shift-list"),
    path(
        'shift-day/<int:pk>/status/<str:status>/change/',
        ShiftDayStatusChange.as_view(),
        name="shift-day-status-change"
    )
]
