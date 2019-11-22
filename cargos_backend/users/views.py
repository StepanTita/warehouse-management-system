from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, DetailView
from notifications.signals import notify

from cargos_main.models import Cargo
from shared_logic.database_queries import get_notifications_unread_first, get_cargos_todate, get_dated_for_user, \
    get_all_notifications
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

    return JsonResponse({
        'notifies_unread': notifies_as_table_unread,
        'notifies_read': notifies_as_table_read,
        'locale': request.LANGUAGE_CODE,
    })


@login_required(login_url='sign_in')
def notify_remove(request):
    notifies_as_table_unread, notifies_as_table_read = notifies_response(request.user,
                                                                         request.GET.get('pk'))

    return JsonResponse({
        'notifies_unread': notifies_as_table_unread,
        'notifies_read': notifies_as_table_read,
        'locale': request.LANGUAGE_CODE,
    })


@login_required(login_url='sign_in')
def notifications_view(request):
    notifs_total = get_notifications_unread_first(request.user)
    paginator = Paginator(notifs_total, NOTIFICATIONS_PER_PAGE)

    page = request.GET.get('page', 0)
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
        return get_all_notifications(self.request.user)


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
