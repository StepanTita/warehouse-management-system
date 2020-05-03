from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, Select, TextInput, MultipleChoiceField
from django.forms.widgets import SelectMultiple

from cargos_main.models import Company

USERS = [(str(user.id), user.username) for user in User.objects.all()]


class CompanyCreationForm(ModelForm):
    employees = MultipleChoiceField(choices=USERS, widget=SelectMultiple(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Company
        fields = ['vendor', 'leader', 'description', 'website']
        widgets = {
            'description': Textarea(attrs={'cols': 30, 'rows': 10, 'class': 'form-control'}),
            'vendor': TextInput(attrs={'class': 'form-control'}),
            'leader': Select(attrs={'class': 'form-control'}),
            'website': TextInput(attrs={'class': 'form-control'})
        }
