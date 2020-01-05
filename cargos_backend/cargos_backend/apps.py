# my_project_app/apps.py
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    menu = (

        ParentItem('Content', children=[
            ChildItem(model='cargos_main.cargo'),
            ChildItem(model='cargos_main.cell'),
            ChildItem(model='cargos_main.storage'),
        ], icon='fa fa-archive'),
        ParentItem('Users', children=[
            ChildItem(model='auth.user'),
        ], icon='fa fa-users'),
        ParentItem('Notifications', children=[
            ChildItem(model='notifications.notification'),
        ], icon='fa fa-exclamation'),
        ParentItem('Right Side Menu', children=[
            ChildItem('Backup', url='backup_view'),
            ChildItem('Password change', url='admin:password_change'),
            ChildItem('Open Google', url='http://google.com', target_blank=True),

        ], align_right=True, icon='fa fa-cog'),
    )
    layout = 'vertical'

    def ready(self):
        super(SuitConfig, self).ready()

        # DO NOT COPY FOLLOWING LINE
        # It is only to prevent updating last_login in DB for demo app
        self.prevent_user_last_login()

    def prevent_user_last_login(self):
        """
        Disconnect last login signal
        """
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(update_last_login)
