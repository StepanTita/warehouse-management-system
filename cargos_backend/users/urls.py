"""cargos_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'users'

urlpatterns = [
    path('signOut/', views.sign_out, name='sign_out'),
    path('signIn/', views.SignInFormView.as_view(), name='sign_in'),
    path('accessDenied/', views.access_denied, name='access_denied'),
    path('notifyCreate/', views.nortify_create, name='notify_create'),
    path('notificationsView/', views.notifications_view, name='notifications_view'),
    path('notificationSingle/<int:pk>/', views.NotificationDetailView.as_view(), name='notification_single'),
    path('notifyIgnore/', views.notify_ignore, name='notify_ignore'),
    path('notifyRemove/', views.notify_remove, name='notify_remove'),
    path('mobileObjects/', views.MobileObjectsView.as_view(), name='mobile_objects'),
    path('mobileNotifications/', views.MobileNotificationsView.as_view(), name='mobile_notifications'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('userIDRequester', views.UserIDRequesterView.as_view(), name='user_id_requester')
]
