import datetime as dt

from django import forms

from shared_logic.choices import CATEGORY_CHOICES, FIELDS_CHOICES
from .models import Storage


class NewCargoForm(forms.Form):
    error_css_class = 'error'
    title = forms.CharField(label="Title", max_length=200)

    storage = forms.ModelChoiceField(queryset=Storage.objects.all(), label="Storage", empty_label="(Nothing)")

    height = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0, localize=True)
    length = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0, localize=True)
    width = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0, localize=True)

    description = forms.CharField(label="Description", max_length=500, widget=forms.Textarea)

    date_added = forms.DateTimeField(initial=dt.datetime.now,
                                     widget=forms.DateTimeInput(  # format=("%Y-%m-%d %H:%M:%S %Z"),
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Select a date'}), localize=True, disabled=True)
    date_dated = forms.DateField(initial=dt.date.today,
                                 widget=forms.DateInput(  #format=('%Y-%m-%d'),
                               attrs={'class': 'form-control',
                                      'placeholder': 'Select a date'}), localize=True)

    rotatable = forms.BooleanField(label='Rotatable', required=False)

    title.widget.attrs.update({'class': 'col-md-7'})
    height.widget.attrs.update({'class': 'col-md-7'})
    length.widget.attrs.update({'class': 'col-md-7'})
    width.widget.attrs.update({'class': 'col-md-7'})
    description.widget.attrs.update({'class': 'col-md-7'})
    storage.widget.attrs.update({'class': 'col-md-7'})


class SearchForm(forms.Form):
    error_css_class = 'error'
    search = forms.CharField(max_length=150, label='Search')

    storages = forms.ModelChoiceField(queryset=Storage.objects.all(), label='Storages', empty_label="(Nothing)")
    category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES)
    fields = forms.MultipleChoiceField(choices=FIELDS_CHOICES, label='Fields')
