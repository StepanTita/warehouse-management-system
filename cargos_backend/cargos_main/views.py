from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

from shared_logic.database_queries import create_search_queryset, get_all_cargos, get_cargo_by_pk
from shared_logic.status_logger.status_logger import view_status_logger, class_status_logger
from shared_logic.util_vars import CARGOS_PER_PAGE
from .cargos_saving import save_cargo
from .forms import NewCargoForm, SearchForm
from .models import Cargo


# @view_status_logger
@login_required(login_url="users:sign_in")
def index(request):
    search_form = SearchForm()
    return render(request, 'main_control/controller/control.html', {'search_form': search_form, 'is_index': True})


@view_status_logger
@login_required(login_url='users:sign_in')
def new_cargo(request):
    search_form = SearchForm()
    if request.method == "POST":
        data = request.POST

        success = save_cargo(data)
        if not success:
            form = NewCargoForm(data or None)
            form.add_error('storage', 'No available space in this storage!')
            return render(request, 'managing_cargos/new_cargo/new_cargo.html',
                          {'form': form, 'search_form': search_form, 'table_name': 'New cargo'})

        form = NewCargoForm()
    else:
        form = NewCargoForm()

    return render(request, 'managing_cargos/new_cargo/new_cargo.html',
                  {'form': form, 'search_form': search_form, 'table_name': 'New cargo'})


@view_status_logger
@login_required(login_url='users:sign_in')
def ret_cargo(request, pk):
    # raise Exception
    search_form = SearchForm()
    context = {'cargo': get_cargo_by_pk(pk), 'search_form': search_form, 'table_name': 'Retrieve cargo'}
    return render(request, 'managing_cargos/ret_cargo/ret_cargo.html', context=context)


class CargoSearchListView(LoginRequiredMixin, ListView):
    login_url = 'users:sign_in'
    model = Cargo
    paginate_by = CARGOS_PER_PAGE
    template_name = 'managing_cargos/preview_cargos/preview_cargos.html'

    def to_get_request(self, ):
        request = [f"{k}={v}" for k, v in self.request.GET.items()]
        return '&'.join(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_params'] = self.to_get_request()
        context['table_name'] = 'Search result'
        context['search_form'] = SearchForm()
        context['table_name'] = 'Search Result'
        return context

    # @class_status_logger
    def get_queryset(self):
        return create_search_queryset(self.request.GET)


class CargoListView(LoginRequiredMixin, ListView):
    login_url = 'users:sign_in'
    model = Cargo
    paginate_by = CARGOS_PER_PAGE
    template_name = 'managing_cargos/preview_cargos/preview_cargos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'View cargos'
        context['search_form'] = SearchForm()
        return context

    @class_status_logger
    def get_queryset(self):
        return get_all_cargos(date_sort_reversed=True)


class CargoUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'users:sign_in'
    model = Cargo
    # form_class = ...
    fields = ['title', 'date_dated', 'description']
    template_name = 'managing_cargos/update_cargo/update_cargo.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['table_name'] = 'Cargo Update'
        return context

    @class_status_logger
    def get_success_url(self):
        return reverse('preview_cargos')

    @class_status_logger
    def get_queryset(self):
        return get_all_cargos()


class CargoDelete(LoginRequiredMixin, DeleteView):
    login_url = 'users:sign_in'
    model = Cargo
    template_name = 'managing_cargos/delete_cargo/delete_cargo.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['table_name'] = 'Cargo Delete'
        return context

    @class_status_logger
    def get_success_url(self):
        return reverse('preview_cargos')

    @class_status_logger
    def get_queryset(self):
        return get_all_cargos()


class CargoDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:sign_in'
    model = Cargo
    template_name = 'managing_cargos/preview_cargos/preview_cargo.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['table_name'] = 'Cargo Details'
        return context

    @class_status_logger
    def get_queryset(self):
        return get_all_cargos()
