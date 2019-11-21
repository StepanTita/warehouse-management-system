from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView
from notifications.signals import notify

from cargos_main.models import Cargo
from shared_logic.database_queries import get_notifications_unread_first
from shared_logic.status_logger.status_logger import view_status_logger, class_status_logger
from shared_logic.util_vars import NOTIFICATIONS_PER_PAGE
from .models import DateNotifications


@view_status_logger
def sign_out(request):
    logout(request)
    return render(request, 'main_auth/index.html')


@view_status_logger
def access_denied(request):
    return render(request, 'access_restrictions/access_denied.html')


# @view_status_logger
@login_required(login_url='sign_in')
def nortify_create(request):
    today = datetime.now().date()
    cargos_dated = Cargo.objects.filter(date_dated__lte=today)

    for cargo in cargos_dated:
        DateNotifications.objects.get_or_create(
            user=request.user,
            cargo=cargo
        )
    unviewed = DateNotifications.objects.filter(viewed=False, user=request.user)

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


def notifications_view(request):
    notifs_total = get_notifications_unread_first(request.user.pk).order_by('-timestamp')
    paginator = Paginator(notifs_total, NOTIFICATIONS_PER_PAGE)

    page = request.GET.get('page', 0)
    notifs_per_page = paginator.get_page(page)

    return render(request, 'notifications_pages/notifications_page.html',
                  {
                      'notifications': notifs_per_page,
                      'table_name': 'Notifications',
                  })


def notification_single(request):
    return render(request, 'notifications_pages/notification_single.html')


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
