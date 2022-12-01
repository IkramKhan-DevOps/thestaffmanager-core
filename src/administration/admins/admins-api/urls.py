from django.urls import path
from .views import ChangeTimesAPI, ShiftListAPIView, ShiftDayStatusChange, SiteByClientListView, ShiftDayClockUpdateView

app_name = 'admins-api'
urlpatterns = [
    path('shift/<int:pk>/times/change/', ChangeTimesAPI.as_view(), name="shift-times-change"),
    path('shifts/', ShiftListAPIView.as_view(), name="shift-list"),
    path('client/<int:pk>/sites/', SiteByClientListView.as_view(), name="site-list-by-client"),
    path(
        'shift-day/<int:pk>/status/<str:status>/change/',
        ShiftDayStatusChange.as_view(),
        name="shift-day-status-change"
    ),
    path(
        'shift-day/<int:pk>/clock/<str:action>/',
        ShiftDayClockUpdateView.as_view(),
        name="shift-day-clock-change"
    )
]
