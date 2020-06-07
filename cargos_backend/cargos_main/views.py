import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, FormView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import bridge.consts as consts
from bridge.context import Context
from bridge.status_logger.status_logger import class_status_logger
from .cargos_saving import save_cargo
from .forms import NewCargoForm
from .models import Cargo


class Index(LoginRequiredMixin, TemplateView):
    login_url = 'users:sign_in'
    model = Cargo
    template_name = 'main_control/controller/control.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ctx = Context.get(self.request)

        context['table_name'] = 'Cargo Delete'
        context['is_index'] = True

        if ctx is not None:
            context['cargos_index'] = \
                ctx.Cargo().of_user(self.request.user).order_by('-date_added').query()[:consts.ITEMS_PER_SLIDE]
            context['cargos_dated_index'] = \
                ctx.Cargo().of_user(self.request.user).to_date(datetime.now().date()).query()[:consts.ITEMS_PER_SLIDE]
        return context


class CargoCreateView(LoginRequiredMixin, FormView):
    login_url = 'users:sign_in'
    template_name = 'managing_cargos/new_cargo/new_cargo.html'
    form_class = NewCargoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'New cargo'
        return context

    def form_valid(self, form):
        success = save_cargo(form.cleaned_data)
        if not success:
            form.add_error('storage', 'No available space in this storage!')
            return self.form_invalid(form)
        return super().form_valid(form)

    @class_status_logger
    def get_success_url(self):
        return reverse('new_cargo')


class RetrieveCargoView(LoginRequiredMixin, TemplateView):
    login_url = 'users:sign_in'
    template_name = 'managing_cargos/ret_cargo/ret_cargo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Retrieve cargo'
        return context


class CargoSearchListView(LoginRequiredMixin, ListView):
    template_name = 'managing_cargos/preview_cargos/preview_cargos.html'
    login_url = 'users:sign_in'
    paginate_by = consts.CARGOS_PER_PAGE
    model = Cargo

    def to_get_request(self):
        request = [f"{k}={v}" for k, v in self.request.GET.items()]
        return '&'.join(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_params'] = self.to_get_request()
        context['table_name'] = 'Search result'
        return context

    def get_queryset(self):
        search = self.request.GET['search']
        storage = self.request.GET['storages']
        fields = self.request.GET.getlist('fields')

        return Context.get(self.request).Search(search, storage, fields)


class SearchRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        search = request.GET.get('search', '')
        storages = [storage.id for storage in Context.get(self.request).Storage().of_user(self.request.user).query()]
        fields = [8, 9]  # FIXME

        search_result = Context.get(self.request).Search(search, storages[0], fields)
        search_json = serializers.serialize("json", search_result)

        json_data = json.loads(search_json)
        result = [obj['fields'] for obj in json_data]
        return Response(result)


class CargoListView(LoginRequiredMixin, ListView):
    login_url = 'users:sign_in'
    model = Cargo
    paginate_by = consts.CARGOS_PER_PAGE
    template_name = 'managing_cargos/preview_cargos/preview_cargos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'View cargos'
        return context

    @class_status_logger
    def get_queryset(self):
        self.paginate_by = int(self.request.GET.get('show', consts.CARGOS_PER_PAGE))
        sort_reversed = self.request.GET.get('sort', '1')
        order = ("-" if sort_reversed else "") + "date_added"
        return Context.get(self.request).Cargo().of_user(self.request.user).order_by(order).query()


class CargoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'managing_cargos/update_cargo/update_cargo.html'
    fields = ['title', 'date_dated', 'description']
    login_url = 'users:sign_in'
    model = Cargo

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Cargo Update'
        return context

    @class_status_logger
    def get_success_url(self):
        return reverse('preview_cargos')

    @class_status_logger
    def get_queryset(self):
        return Context.get(self.request).Cargo().of_user(self.request.user).query()


class CargoDelete(LoginRequiredMixin, DeleteView):
    template_name = 'managing_cargos/delete_cargo/delete_cargo.html'
    login_url = 'users:sign_in'
    model = Cargo

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Cargo Delete'
        return context

    @class_status_logger
    def get_success_url(self):
        return reverse('preview_cargos')

    @class_status_logger
    def get_queryset(self):
        return Context.get(self.request).Cargo().of_user(self.request.user).query()


class CargoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'managing_cargos/preview_cargos/preview_cargo.html'
    login_url = 'users:sign_in'
    model = Cargo

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Cargo Details'
        return context

    @class_status_logger
    def get_queryset(self):
        return Context.get(self.request).Cargo().of_user(self.request.user).query()
