import json
from datetime import datetime
from functools import wraps

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, DetailView
from notifications.models import Notification
from notifications.signals import notify
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cargos_main.forms import SearchForm
from cargos_main.models import Cargo
from shared_logic.database_queries import get_notifications_unread_first, get_cargos_todate, get_dated_for_user, \
    get_all_notifications, get_cargo_by_pk
from shared_logic.status_logger.status_logger import view_status_logger, class_status_logger
from shared_logic.util_vars import NOTIFICATIONS_PER_PAGE
from users.notifies_response import notifies_response


@view_status_logger
def sign_out(request):
    logout(request)
    return render(request, 'main_auth/index.html')


@view_status_logger
def access_denied(request):
    return render(request, 'access_restrictions/access_denied.html')


@view_status_logger
@login_required(login_url='sign_in')
def nortify_create(request):
    today = datetime.now().date()
    cargos_dated = get_cargos_todate(today)

    unviewed = get_dated_for_user(cargos_dated, request.user)

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
    notifs_total = get_notifications_unread_first(request.user,
                                                  reversed=True if request.GET.get('sort', '1') == '1' else False)
    paginator = Paginator(notifs_total, int(request.GET.get('show', NOTIFICATIONS_PER_PAGE)))

    page = request.GET.get('page', 1)
    notifs_per_page = paginator.get_page(page)

    return render(request, 'notifications_pages/notifications_page.html',
                  {
                      'notifications': notifs_per_page,
                      'table_name': 'Notifications',
                      'is_notifies': True,
                      'search_form': SearchForm()
                  })


class NotificationDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:sign_in'
    model = Cargo
    template_name = 'notifications_pages/notification.html'

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_notify_single'] = True
        context['search_form'] = SearchForm()
        return context

    @class_status_logger
    def get_queryset(self):
        return get_all_notifications(self.request.user)


class SignInFormView(FormView):
    form_class = AuthenticationForm
    # form_class = CustomAuthenticationForm
    template_name = "user_actions/signIn.html"

    @class_status_logger
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = "Sign In"
        return context

    @class_status_logger
    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    @class_status_logger
    def get_success_url(self):
        return reverse('index')


# ------------------------MOBILE----------------------------


def csrf_exempt(view_func):
    """Mark a view function as being exempt from the CSRF view protection."""

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
    return HttpResponse("Error")


class MobileObjectsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = serializers.serialize("json", Cargo.objects.all())
        json_data = json.loads(data)
        result = [obj['fields'] for obj in json_data]
        return Response(result)

    def post(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class MobileNotificationsView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get_cargo_name_safe(self, pk):
        cargo_name = "Not found"
        try:
            cargo_name = get_cargo_by_pk(pk).title
        except ObjectDoesNotExist:
            ...
        return cargo_name

    def get(self, request):
        if not request.GET:
            data = serializers.serialize("json", Notification.objects.filter(recipient=request.user.id))
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
            new_ser = serializers.serialize("json", new)
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
