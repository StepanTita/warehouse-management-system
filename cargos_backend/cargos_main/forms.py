import datetime as dt

from django import forms

from bridge import context
from bridge.choices import FIELDS_CHOICES
from .models import Storage

DECIMAL_FORMAT = dict(decimal_places=2,
                      max_digits=9,
                      min_value=0.01,
                      max_value=100,
                      localize=True,
                      widget=forms.NumberInput())


class NewCargoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        if request:
            self.fields['storage'].queryset = context.Context.get(request).Storage().of_user(request.user).query()

    error_css_class = 'has-error'
    title = forms.CharField(label="Title", max_length=200, required=False)

    storage = forms.ModelChoiceField(queryset=Storage.objects.all(),
                                     label="Storage",
                                     empty_label="...",
                                     required=True)

    height = forms.DecimalField(**DECIMAL_FORMAT)

    length = forms.DecimalField(**DECIMAL_FORMAT)

    width = forms.DecimalField(**DECIMAL_FORMAT)

    description = forms.CharField(label="Description", max_length=500, required=False)

    date_added = forms.DateTimeField(
        initial=dt.datetime.now,
        localize=True,
        required=True
    )

    date_dated = forms.DateField(
        required=True,
        initial=dt.datetime.now,
        localize=True
    )

    rotatable = forms.BooleanField(label='Rotatable', required=False, widget=forms.NullBooleanSelect)

    # Widgets
    title.widget = forms.TextInput()
    description.widget = forms.Textarea()
    storage.widget = forms.Select()

    date_added.widget.attrs.update({'placeholder': 'Select a date', 'type': 'date'})
    date_dated.widget.attrs.update({'placeholder': 'Select a date', 'type': 'date'})

    height.widget.attrs.update({'placeholder': '0.01...100', })
    length.widget.attrs.update({'placeholder': '0.01...100', })
    width.widget.attrs.update({'placeholder': '0.01...100', })

    description.widget.attrs.update({'placeholder': 'The cargo description...'})
    title.widget.attrs.update({'placeholder': 'The cargo title...'})


class SearchForm(forms.Form):
    error_css_class = 'error'
    search = forms.CharField(
        max_length=150,
        label='Search',
    )

    storages = forms.ModelChoiceField(
        queryset=Storage.objects.all(),
        label='Storages', empty_label="...",
    )

    fields = forms.MultipleChoiceField(
        choices=FIELDS_CHOICES,
        label='Fields',
    )

    # Widgets
    search.widget = forms.TextInput(attrs={
        'class': 'form-control col-md-6 text text-secondary',
        'placeholder': 'Search here...'
    })

    storages.widget = forms.Select(attrs={
        'class': 'form-control text text-secondary col-md-4',
    })

    fields.widget = forms.SelectMultiple(attrs={
        'class': 'form-control col-md-2 text text-secondary selectpicker',
    })
