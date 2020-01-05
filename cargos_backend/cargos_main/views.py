import json
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_logic.database_queries import create_search_queryset, get_all_cargos, get_cargo_by_pk, get_cargos_todate, \
    get_all_storages
from shared_logic.iot_logic import IOT_URL, get_free_pos, get_occupied
from shared_logic.status_logger.status_logger import view_status_logger, class_status_logger
from shared_logic.util_vars import CARGOS_PER_PAGE
from .cargos_saving import save_cargo
from .forms import NewCargoForm, SearchForm
from .models import Cargo


# @view_status_logger
@login_required(login_url="users:sign_in")
def index(request):
    search_form = SearchForm()
    return render(request, 'main_control/controller/control.html',
                  {
                      'search_form': search_form,
                      'is_index': True,
                      'cargos_index': get_all_cargos(date_sort_reversed=True)[:4],
                      'cargos_dated_index': get_cargos_todate(datetime.now().date())[:4],
                  })


# @view_status_logger
@login_required(login_url='users:sign_in')
def new_cargo(request):
    search_form = SearchForm()
    if request.method == "POST":
        data = request.POST

        pos = get_free_pos()
        success = save_cargo(data)
        if not success or pos < 0:
            form = NewCargoForm(data or None)
            form.add_error('storage', 'No available space in this storage!')
            return render(request, 'managing_cargos/new_cargo/new_cargo.html',
                          {'form': form, 'search_form': search_form, 'table_name': 'New cargo'})

        PARAMS = {'pos': pos}
        # sending get request and saving the response as response object
        r = requests.get(url=IOT_URL, params=PARAMS)
        form = NewCargoForm()
    else:
        form = NewCargoForm()

    return render(request, 'managing_cargos/new_cargo/new_cargo.html',
                  {'form': form, 'search_form': search_form, 'table_name': 'New cargo'})


@view_status_logger
@login_required(login_url='users:sign_in')
def ret_cargo(request, pk):
    # defining a params dict for the parameters to be sent to the API
    search_form = SearchForm()
    context = {'cargo': get_cargo_by_pk(pk), 'search_form': search_form, 'table_name': 'Retrieve cargo'}

    pos = get_occupied()
    if pos < 0:
        ...
        return render(request, 'managing_cargos/ret_cargo/ret_cargo.html', context=context)
    PARAMS = {'pos': pos}
    # sending get request and saving the response as response object
    r = requests.get(url=IOT_URL, params=PARAMS)
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
        search = self.request.GET['search']
        storage = self.request.GET['storages']
        fields = self.request.GET.getlist('fields')
        return create_search_queryset(search, storage, fields)


class SearchRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_cargo_name_safe(self, pk):
        cargo_name = "Not found"
        try:
            cargo_name = get_cargo_by_pk(pk).title
        except ObjectDoesNotExist:
            ...
        return cargo_name

    def get(self, request):
        search = request.GET.get('search', '')
        storages = [storage.id for storage in get_all_storages()]
        fields = [8, 9]

        search_result = create_search_queryset(search, storages[0], fields)
        search_json = serializers.serialize("json", search_result)

        json_data = json.loads(search_json)
        result = [obj['fields'] for obj in json_data]
        return Response(result)


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
        self.paginate_by = int(self.request.GET.get('show', CARGOS_PER_PAGE))
        sort_reversed = self.request.GET.get('sort', '1')
        return get_all_cargos(date_sort_reversed=True if sort_reversed == '1' else False)


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
