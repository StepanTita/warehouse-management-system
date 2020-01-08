from django import forms
from django.conf import settings

from .utils import backup_database, backup_media


class DatabaseBackupForm(forms.Form):
    database = forms.ChoiceField(
        label='Pick a database to backup',
        choices=zip(
            settings.DATABASES.keys(),
            settings.DATABASES.keys()
        ),
        widget=forms.Select(attrs={'class': 'form-control col-md-7'})
    )

    def do_backup(self):
        return backup_database(self.cleaned_data['database'])


class MediaBackupForm(forms.Form):

    def do_backup(self):
        return backup_media()
