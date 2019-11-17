from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

from shared_logic.status_logger.status_logger import view_status_logger, class_status_logger
from shared_logic.util_vars import cargos_per_page
from .cargos_saving import save_cargo
from .forms import NewCargoForm, SearchForm
from .models import Cargo


@view_status_logger
@login_required(login_url="users:sign_in")
def index(request):
    form = SearchForm(request.POST or None)
    return render(request, 'main_control/controller/control.html', {'form': form})


@view_status_logger
@login_required(login_url='users:sign_in')
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
@login_required(login_url='users:sign_in')
def ret_cargo(request):
    # raise Exception
    if request.method == "POST":
        pass  # TODO
    else:
        return render(request, 'main_control/ret_cargo/ret_cargo.html')


class CargoSearchListView(LoginRequiredMixin, ListView):
    login_url = 'users:sign_in'
    model = Cargo
    paginate_by = cargos_per_page
    template_name = 'managing_cargos/preview_cargos/preview_cargos.html'

    @class_status_logger
    def get_queryset(self):
        category = self.request.GET.get('category')
        if category == '1':
            print('OK')
            search = self.request.GET.get('search')
            storage = self.request.GET.get('storages')
            fields = self.request.GET.get_list('fields')
            return Cargo.objects.all().filter()
        else:
            raise NotImplementedError


class CargoListView(LoginRequiredMixin, ListView):
    login_url = 'users:sign_in'
    model = Cargo
    paginate_by = cargos_per_page
    template_name = 'managing_cargos/preview_cargos/preview_cargos.html'

    @class_status_logger
    def get_queryset(self):
        return Cargo.objects.all().order_by("-date_added")


class CargoUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'users:sign_in'
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
    login_url = 'users:sign_in'
    model = Cargo
    template_name = 'managing_cargos/delete_cargo/delete_cargo.html'

    @class_status_logger
    def get_success_url(self):
        return reverse('preview_cargos')

    @class_status_logger
    def get_queryset(self):
        return Cargo.objects.all()


class CargoDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:sign_in'
    model = Cargo
    template_name = 'managing_cargos/preview_cargos/preview_cargo.html'

    @class_status_logger
    def get_queryset(self):
        return Cargo.objects.all()

