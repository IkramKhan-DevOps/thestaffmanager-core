from django.urls import path
from .views import LoginView, LogoutView, UserUpdateView, UserPasswordChange, ForgetPasswordView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('password/change/', UserPasswordChange.as_view(), name='user-password-change'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
]
