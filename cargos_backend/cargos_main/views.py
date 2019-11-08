from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

from .cargos_saving import save_cargo
from .custom_logic.util_vars import cargos_per_page
from .forms import NewCargoForm, SearchForm
from .models import Cargo
from .status_logger.status_logger import view_status_logger, class_status_logger


@view_status_logger
@login_required(login_url="sign_in")
def index(request):
    form = SearchForm(request.POST or None)
    return render(request, 'main_control/controller/control.html', {'form': form})


@view_status_logger
@login_required(login_url='sign_in')
def new_cargo(request):
    if request.method == "POST":
        data = request.POST

        success = save_cargo(data)
        if not success:
            form = NewCargoForm(data or None)
            form.add_error('storage', 'No available space in this storage!')
            return render(request, 'managing_cargos/new_cargo/new_cargo.html', {'form': form.as_table()})

        form = NewCargoForm()

        return render(request, 'managing_cargos/new_cargo/new_cargo.html', {'form': form.as_table()})
    else:
        form = NewCargoForm()
        return render(request, 'managing_cargos/new_cargo/new_cargo.html', {'form': form.as_table()})


@view_status_logger
@login_required(login_url='sign_in')
def ret_cargo(request):
    if request.method == "POST":
        pass  # TODO
    else:
        return render(request, 'main_control/ret_cargo/ret_cargo.html')


@view_status_logger
def access_denied(request):
    return render(request, 'access_restrictions/access_denied.html')


@view_status_logger
def sign_out(request):
    logout(request)
    return render(request, 'main_auth/index.html')


class CargoListView(LoginRequiredMixin, ListView):
    login_url = 'sign_in'
    model = Cargo
    paginate_by = cargos_per_page
    template_name = 'managing_cargos/preview_cargos/preview_cargos.html'

    @class_status_logger
    def get_queryset(self):
        return Cargo.objects.all().order_by("-date_added")


class CargoUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'sign_in'
    model = Cargo
    # form_class = ...
    fields = ['title', 'date_dated', 'description']
    template_name = 'managing_cargos/update_cargo/update_cargo.html'

    @class_status_logger
    def get_success_url(self):
        return reverse('preview_cargos')

    @class_status_logger
    def get_queryset(self):
        return Cargo.objects.all()


class CargoDelete(LoginRequiredMixin, DeleteView):
    login_url = 'sign_in'
    model = Cargo
    template_name = 'managing_cargos/delete_cargo/delete_cargo.html'

    @class_status_logger
    def get_success_url(self):
        return reverse('preview_cargos')

    @class_status_logger
    def get_queryset(self):
        return Cargo.objects.all()


class CargoDetailView(LoginRequiredMixin, DetailView):
    login_url = 'sign_in'
    model = Cargo
    template_name = 'managing_cargos/preview_cargos/preview_cargo.html'

    @class_status_logger
    def get_queryset(self):
        return Cargo.objects.all()

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['cells_list'] = Cell.objects.all()
    #     return context


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

# def preview_cargos(request):
#     print('Hi')
#     if request.method == "GET":
#         success = True
#         data = request.GET
#
#         result = Cargo.objects.get(title__contains=data['title'])
#         print(result)
#         if success:
#             return render(request, 'preview_cargos/preview_cargos.html', {'cargo_list': result})
#         else:
#             return render(request, 'preview_cargos/preview_cargos.html')
#     else:
#         return render(request, 'preview_cargos/preview_cargos.html')


# class SignUpFormView(FormView):
#     form_class = UserCreationForm
#     # form_class = CustomUserCreationForm
#     template_name = "user_actions/signUp.html"
#
#     def get_success_url(self):
#         return reverse('sign_in')
