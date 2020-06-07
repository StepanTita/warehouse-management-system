from django import forms
from django.contrib.auth.models import User
from django.forms import widgets

from cargos_main.models import Company
from users.models import Employee

USERS = [(str(user.id), user.username) for user in User.objects.all()]


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['vendor', 'leader', 'description', 'website', 'logo']
        widgets = {
            'description': widgets.Textarea(attrs={'cols': 30, 'rows': 10, 'class': 'form-control'}),
            'vendor': widgets.TextInput(attrs={'class': 'form-control'}),
            'leader': widgets.Select(attrs={'class': 'form-control'}),
            'website': widgets.TextInput(attrs={'class': 'form-control'}),
            'logo': widgets.FileInput(attrs={'class': 'form-control'})
        }


class EmployeeForm(forms.ModelForm):
    facebook = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    github = forms.URLField(required=False)
    linkedin = forms.URLField(required=False)

    class Meta:
        model = Employee
        fields = ['company', 'image', 'facebook', 'twitter', 'github', 'linkedin']
        widgets = {
            'company': widgets.Select(attrs={'class': 'form-control'}),
            'image': widgets.FileInput(attrs={'class': 'form-control'}),
            'facebook': widgets.URLInput(attrs={'class': 'form-control'}),
            'twitter': widgets.URLInput(attrs={'class': 'form-control'}),
            'github': widgets.URLInput(attrs={'class': 'form-control'}),
            'linkedin': widgets.URLInput(attrs={'class': 'form-control'}),
        }
