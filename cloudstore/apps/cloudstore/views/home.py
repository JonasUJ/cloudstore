from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(LoginRequiredMixin, View):
    '''Main landing page - only available when logged in'''

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'home/home.html')
