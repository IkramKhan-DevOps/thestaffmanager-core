from django.urls import path
from src.website.views import HomeView

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name="home")
]
