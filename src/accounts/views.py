from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from src.administration.admins.forms import UserProfileForm


class CrossAuth(View):

    def get(self, request):

        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admins:dashboard')
            else:
                return redirect('employees:dashboard')

        return redirect("accounts:login")


class LoginView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect("accounts:cross-auth")

        form = AuthenticationForm()
        return render(request, template_name='accounts/login.html', context={'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("accounts:cross-auth")
        return render(request, template_name='accounts/login.html', context={'form': form})


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/accounts/login/')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)


class UserPasswordChange(View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        context = {'form': form}
        return render(request, template_name='accounts/password_change_form.html', context=context)

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            messages.success(request, "Your password changed successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/password_change_form.html', context=context)