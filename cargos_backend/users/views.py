import json
from datetime import datetime
from functools import wraps

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, DetailView, ListView
from notifications.models import Notification
from notifications.signals import notify
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import bridge.database_queries as queries
from bridge import context
from bridge.consts import NOTIFICATIONS_PER_PAGE, COMPANIES_PER_PAGE
from bridge.helpers.company_helper import count_cargos_for_company, count_employees_for_company
from bridge.status_logger.status_logger import view_status_logger, class_status_logger
from cargos_main.models import Cargo, Company
from users.forms import CompanyCreationForm, EmployeeForm
from users.models import Employee
from users.notifies_response import notifies_response


@view_status_logger
def sign_out(request):
    logout(request)
    return render(request, 'main_auth/index.html')


@view_status_logger
def access_denied(request):
    return render(request, 'access_restrictions/../bridge/templates/utils/includes/errors/access_denied.html')


@view_status_logger
@login_required(login_url='sign_in')
def nortify_create(request):
    today = datetime.now().date()
    cargos_dated = queries.get_cargos_todate(company=queries.get_company(request.user), date=today)

    unviewed = queries.get_dated_for_user(cargos_dated, request.user)

    for notification in unviewed:
        notify.send(
            notification.cargo,
            recipient=[notification.user],
            verb=f'Cargo: {notification.cargo.title}, has spoilt'
        )
        # notification.delete()
        notification.viewed = True
        notification.save()

    return JsonResponse({'unviewed': f'{len(unviewed)}'})


@login_required(login_url='sign_in')
def notify_ignore(request):
    notifies_as_table_unread, notifies_as_table_read = notifies_response(request.user,
                                                                         request.GET.get('pk'),
                                                                         request.GET.get('ignore'))
    show = int(request.GET.get('show', 5))
    return JsonResponse({
        'notifies_unread': notifies_as_table_unread[:show],
        'notifies_read': notifies_as_table_read[:show - len(notifies_as_table_unread[:show])],
        'locale': request.LANGUAGE_CODE,
    })


@login_required(login_url='sign_in')
def notify_remove(request):
    notifies_as_table_unread, notifies_as_table_read = notifies_response(request.user,
                                                                         request.GET.get('pk'))
    show = int(request.GET.get('show', 5))
    return JsonResponse({
        'notifies_unread': notifies_as_table_unread[:show],
        'notifies_read': notifies_as_table_read[:show - len(notifies_as_table_unread[:show])],
        'locale': request.LANGUAGE_CODE,
    })


@login_required(login_url='sign_in')
def notifications_view(request):
    notifs_total = queries.get_notifications_unread_first(request.user,
                                                          reversed=True if request.GET.get('sort',
                                                                                           '1') == '1' else False)
    paginator = Paginator(notifs_total, int(request.GET.get('show', NOTIFICATIONS_PER_PAGE)))

    page = request.GET.get('page', 1)
    notifs_per_page = paginator.get_page(page)

    return render(request, 'notifications_pages/notifications_page.html',
                  {
                      'notifications': notifs_per_page,
                      'table_name': 'Notifications',
                      'is_notifies': True,
                  })


class NotificationDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:sign_in'
    model = Cargo
    template_name = 'notifications_pages/notification.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_notify_single'] = True
        return context

    @class_status_logger
    def get_queryset(self):
        return queries.get_all_notifications(self.request.user)


class SignInFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'user_actions/signIn.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Sign In'
        if 'action' in self.request.GET:
            logout(self.request)
        return context

    @class_status_logger
    def form_valid(self, form):
        login(self.request, form.get_user())
        ctx = context.Context.get(self.request)
        if ctx is None:
            raise AssertionError
        return redirect(self.get_success_url())

    @class_status_logger
    def get_success_url(self):
        return reverse('index')


class SignUpFormView(FormView):
    form_class = UserCreationForm
    template_name = 'user_actions/signUp.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Sign Up'
        if 'action' in self.request.GET:
            logout(self.request)
        return context

    @class_status_logger
    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

    @class_status_logger
    def get_success_url(self):
        return reverse('index')


class PersonalPage(View):
    template_name = 'user_actions/personal_page.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['employee'] = Employee.objects.get(user__username=kwargs['username'])
        context['position'] = ", ".join(map(str, context['employee'].position.all())).capitalize()
        context['user_obj'] = Employee.objects.get(id=self.request.user.id)
        return context

    def get(self, request, username):
        return render(request, self.template_name, self.get_context_data(username=username))


class PersonalEdit(LoginRequiredMixin, FormView):
    login_url = 'users:sign_in'
    form_class = EmployeeForm
    template_name = 'user_actions/personal_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Edit personal data'
        if 'action' in self.request.GET:
            logout(self.request)
        return context

    def form_valid(self, form):
        # form.fields['user'] = self.request.user
        # form.user_id = self.request.user
        # form.save()

        employee = Employee.objects.get(id=self.request.user.id)
        employee.company = form.cleaned_data.get('company')
        # employee.image = form.data.get('image')
        employee.facebook = form.cleaned_data.get('facebook')
        employee.twitter = form.cleaned_data.get('twitter')
        employee.linkedin = form.cleaned_data.get('linkedin')
        employee.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class CompanyRegisterFormView(LoginRequiredMixin, FormView):
    login_url = 'users:sign_in'
    form_class = CompanyCreationForm
    template_name = 'company_management/create_company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = 'Create Company'
        if 'action' in self.request.GET:
            logout(self.request)
        return context

    def form_valid(self, form):
        new_company = form.save()  # TODO check that leader is free
        Employee.objects.create(user=form.cleaned_data.get('leader'), company=new_company).save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class CompaniesPreviewView(LoginRequiredMixin, ListView):
    login_url = 'users:sign_in'
    model = Company
    paginate_by = COMPANIES_PER_PAGE
    template_name = 'company_management/preview_companies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = queries.get_all_companies()

        context['cargos'] = dict()
        context['employees'] = dict()
        context['categories'] = dict()
        for cmp in companies:
            context['cargos'][cmp.id] = count_cargos_for_company(cmp)
            context['employees'][cmp.id] = count_employees_for_company(cmp)
            context['categories'][cmp.id] = queries.get_categories(cmp)

        context['employee'] = Employee.objects.get(id=self.request.user.id)
        context['position'] = ", ".join(map(str, context['employee'].position.all())).capitalize()
        context['popular_companies'] = companies  # TODO Popular companies
        context['category_list'] = queries.get_all_categories()
        return context


class CompanyPreviewView(LoginRequiredMixin, DetailView):
    login_url = 'users:sign_in'
    model = Company
    template_name = 'company_management/preview_company.html'

    @class_status_logger
    def get_queryset(self):
        return queries.get_all_companies()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = kwargs['object']

        context['cargos_count'] = count_cargos_for_company(company)
        context['employees_count'] = count_employees_for_company(company)
        context['categories'] = queries.get_categories(company)
        context['employees'] = queries.get_employees(company)

        context['employee'] = Employee.objects.get(id=company.leader.id)
        context['position'] = ", ".join(map(str, context['employee'].position.all())).capitalize()
        context['popular_companies'] = queries.get_all_companies()  # TODO Popular companies
        context['category_list'] = queries.get_all_categories()

        return context


# ------------------------MOBILE----------------------------


def csrf_exempt(view_func):
    '''Mark a view function as being exempt from the CSRF view protection.'''

    # view_func.csrf_exempt = True would also work, but decorators are nicer
    # if they don't have side effects, so return a new function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.csrf_exempt = True
    return wraps(view_func)(wrapped_view)


@csrf_exempt
def authentificate_mobile(request):
    json_data = json.loads(request.body)
    if request.method == 'POST':
        user_login = json_data['login']
        password = json_data['password']
        try:
            found_user = User.objects.get(username=user_login, password=password)
        except Exception:
            found_user = False

        return HttpResponse(found_user is None)
    return HttpResponse('Error')


class MobileObjectsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = serializers.serialize('json', Cargo.objects.all())
        json_data = json.loads(data)
        result = [obj['fields'] for obj in json_data]
        return Response(result)

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class MobileNotificationsView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get_cargo_name_safe(self, pk):
        cargo_name = 'Not found'
        try:
            cargo_name = queries.get_cargo_by_pk(pk).title
        except ObjectDoesNotExist:
            ...
        return cargo_name

    def get(self, request):
        if not request.GET:
            data = serializers.serialize('json', Notification.objects.filter(recipient=request.user.id))
            json_data = json.loads(data)
            result = [obj['fields'] for obj in json_data]
            result = [{'verb': notif['verb'], 'target': self.get_cargo_name_safe(notif['actor_object_id'])} for notif in
                      result]
            return Response(result)
        else:
            data = Notification.objects.filter(recipient=request.user.id)
            new = []
            for notif in data:
                if not notif.emailed:
                    notif.emailed = True
                    notif.save()
                    new.append(notif)
            new_ser = serializers.serialize('json', new)
            json_data = json.loads(new_ser)
            result = [obj['fields'] for obj in json_data]
            result = [{'verb': notif['verb'], 'target': self.get_cargo_name_safe(notif['actor_object_id'])} for notif in
                      result]
            return Response(result)

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserIDRequesterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'id': request.user.id}
        return Response(content)
