import datetime as dt

from django import forms

from shared_logic.choices import FIELDS_CHOICES
from .models import Storage


class NewCargoForm(forms.Form):
    error_css_class = 'has-error'
    title = forms.CharField(label="Title", max_length=200)

    storage = forms.ModelChoiceField(queryset=Storage.objects.all(), label="Storage", empty_label="(Nothing)")

    height = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0, localize=True,
                                widget=forms.NumberInput(attrs={'class': 'col-md-7 form-control form-control-sm'}))
    length = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0, localize=True,
                                widget=forms.NumberInput(attrs={'class': 'col-md-7 form-control form-control-sm'}))
    width = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0, localize=True,
                               widget=forms.NumberInput(attrs={'class': 'col-md-7 form-control form-control-sm'}))

    description = forms.CharField(label="Description", max_length=500)

    date_added = forms.DateTimeField(initial=dt.datetime.now, localize=True, disabled=True)
    date_dated = forms.DateField(initial=dt.date.today, localize=True)

    rotatable = forms.BooleanField(label='Rotatable', required=False)

    title.widget = forms.TextInput(attrs={'class': 'col-md-7 form-control form-control-sm'})
    description.widget = forms.Textarea(attrs={'class': 'col-md-7 form-control form-control-sm'})
    storage.widget = forms.Select(attrs={'class': 'col-md-7 form-control form-control-sm'})

    date_added.widget.attrs.update({'class': 'form-control',
                                    'placeholder': 'Select a date'})
    date_dated.widget.attrs.update({'class': 'form-control',
                                    'placeholder': 'Select a date'})


class SearchForm(forms.Form):
    error_css_class = 'error'
    search = forms.CharField(max_length=150, label='Search', widget=forms.TextInput(attrs={
        'class': 'form-control form-control-sm',
    }))

    storages = forms.ModelChoiceField(queryset=Storage.objects.all(), label='Storages', empty_label="(Nothing)",
                                      widget=forms.Select(attrs={
                                          'class': 'form-control form-control-sm',
                                      }))
    # category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES, widget=forms.Select(attrs={
    #                                       'class': 'form-control form-control-sm',
    #                                   }))

    fields = forms.MultipleChoiceField(choices=FIELDS_CHOICES, label='Fields',
                                       widget=forms.SelectMultiple(attrs={
                                           'class': 'form-control form-control-sm',
                                           'multiple': 'multiple',
                                           'size': '3'
                                       }))
