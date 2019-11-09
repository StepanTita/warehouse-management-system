from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView

from cargos_main.models import Cargo
from shared_logic.status_logger.status_logger import view_status_logger, class_status_logger
from .models import DateNotifications


@view_status_logger
def sign_out(request):
    logout(request)
    return render(request, 'main_auth/index.html')


@view_status_logger
def access_denied(request):
    return render(request, 'access_restrictions/access_denied.html')


@view_status_logger
@login_required(login_url='sign_in')
def norify_create(request):
    pk = request.GET.get('pk')
    new_notification = DateNotifications.objects.create(
        user=request.user,
        cargo=Cargo.objects.get(pk=pk)
    )
    return JsonResponse({'created': 'New product has spoil warning!'})


@view_status_logger
@login_required(login_url='sign_in')
def nortify_need(request):
    today = datetime.now().date()
    cargos_dated = Cargo.objects.filter(data_dated__exact=today, viewed__exact=False)

    if len(cargos_dated) > 0:
        return redirect('notify_create')

    return JsonResponse({''})


class SignInFormView(FormView):
    form_class = AuthenticationForm
    # form_class = CustomAuthenticationForm
    template_name = "user_actions/signIn.html"

    @class_status_logger
    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    @class_status_logger
    def get_success_url(self):
        return reverse('index')
