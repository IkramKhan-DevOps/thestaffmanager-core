from django.urls import path
from .views import ChangeTimesAPI, ShiftListAPIView

app_name = 'admins-api'
urlpatterns = [
    path('shift/<int:pk>/times/change/', ChangeTimesAPI.as_view(), name="shift-times-change"),
    path('shifts/', ShiftListAPIView.as_view(), name="shift-list"),
]
