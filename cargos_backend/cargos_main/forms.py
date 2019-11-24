import datetime as dt

from django import forms

from shared_logic.choices import FIELDS_CHOICES
from .models import Storage


class NewCargoForm(forms.Form):
    error_css_class = 'has-error'
    title = forms.CharField(label="Title", max_length=200, required=False)

    storage = forms.ModelChoiceField(queryset=Storage.objects.all(), label="Storage", empty_label="(Nothing)")

    height = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0.01, max_value=100, localize=True,
                                widget=forms.NumberInput())
    length = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0.01, max_value=100, localize=True,
                                widget=forms.NumberInput())
    width = forms.DecimalField(decimal_places=2, max_digits=9, min_value=0.01, max_value=100, localize=True,
                               widget=forms.NumberInput())

    description = forms.CharField(label="Description", max_length=500, required=False)

    date_added = forms.DateTimeField(initial=dt.datetime.now, localize=True,
                                     widget=forms.TextInput(
                                         attrs={'type': 'date'}
                                     ), required=False)
    date_dated = forms.DateField(
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'date', 'value': '111'}
        ),
        initial=dt.datetime.now,
        localize=True
    )

    rotatable = forms.BooleanField(label='Rotatable', required=False)

    # Widgets
    title.widget = forms.TextInput()
    description.widget = forms.Textarea()
    storage.widget = forms.Select()

    date_added.widget.attrs.update({'placeholder': 'Select a date', })
    date_dated.widget.attrs.update({'placeholder': 'Select a date', 'class': 'col-md-7'})

    height.widget.attrs.update({'placeholder': '0.01...100', })
    length.widget.attrs.update({'placeholder': '0.01...100', })
    width.widget.attrs.update({'placeholder': '0.01...100', })

    description.widget.attrs.update({'placeholder': 'The cargo description...'})
    title.widget.attrs.update({'placeholder': 'The cargo title...'})


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
