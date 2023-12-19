from django.urls import path

from .views import (
    ScheduleView, ShiftAddModelView
)

app_name = "schedular"
urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    path('model/shift/add/', ShiftAddModelView.as_view(), name='model_shift_add'),
]
