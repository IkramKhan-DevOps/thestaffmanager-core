from django.urls import path
from .views import LoginView, LogoutView, UserUpdateView, UserPasswordChange, CrossAuth

app_name = 'accounts'
urlpatterns = [
    path('cross-auth/', CrossAuth.as_view(), name='cross-auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('password/change/', UserPasswordChange.as_view(), name='user-password-change'),
]
