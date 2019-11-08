from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView

from shared_logic.status_logger.status_logger import view_status_logger, class_status_logger


@view_status_logger
def sign_out(request):
    logout(request)
    return render(request, 'main_auth/index.html')


@view_status_logger
def access_denied(request):
    return render(request, 'access_restrictions/access_denied.html')


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
