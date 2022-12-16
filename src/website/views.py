from django.shortcuts import redirect
from django.views import View


class HomeView(View):

    def get(self, request):
        return redirect("accounts:cross-auth")
