from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import FormView

# Create your views here.


def access_denied(request):
    return render(request, 'access_restrictions/access_denied.html')


@login_required(login_url="sign_in")
def index(request):
    return render(request, 'main_auth/index.html')


def sign_out(request):
    logout(request)
    return render(request, 'main_auth/index.html')


class SignUpFormView(FormView):
    form_class = UserCreationForm
    # form_class = CustomUserCreationForm
    template_name = "user_actions/signUp.html"

    def get_success_url(self):
        return reverse('sign_in')


class SignInFormView(FormView):
    form_class = AuthenticationForm
    # form_class = CustomAuthenticationForm
    template_name = "user_actions/signIn.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')

