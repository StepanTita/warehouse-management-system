from django import forms
import datetime as dt
from .models import Cell


class NewCargoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)

    cell = forms.ModelChoiceField(queryset=Cell.objects.all(), label="Cell")

    # row = forms.IntegerField(label="Row")
    # elevation = forms.IntegerField(label="Elevation")
    # position = forms.IntegerField(label="Position")

    height = forms.DecimalField(decimal_places=2, max_digits=9)
    length = forms.DecimalField(decimal_places=2, max_digits=9)
    width = forms.DecimalField(decimal_places=2, max_digits=9)

    description = forms.CharField(label="Description", max_length=500, widget=forms.Textarea)

    date_added = forms.DateTimeField(initial=dt.datetime.now,
        widget=forms.DateTimeInput(format=("%Y-%m-%d %H:%M:%S %Z"),
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Select a date'}))
    date_dated = forms.DateField(initial=dt.date.today,
        widget=forms.DateInput(format=('%Y-%m-%d'),
                               attrs={'class': 'form-control',
                                      'placeholder': 'Select a date'}))

    title.widget.attrs.update({'class': 'col-md-7'})
    # row.widget.attrs.update({'class': 'col-md-7'})
    # elevation.widget.attrs.update({'class': 'col-md-7'})
    # position.widget.attrs.update({'class': 'col-md-7'})
    height.widget.attrs.update({'class': 'col-md-7'})
    length.widget.attrs.update({'class': 'col-md-7'})
    width.widget.attrs.update({'class': 'col-md-7'})
    description.widget.attrs.update({'class': 'col-md-7'})
    cell.widget.attrs.update({'class': 'col-md-7'})
    # date_added.widget.attrs.update({'class': 'col-md-7'})
    # date_dated.widget.attrs.update({'class': 'col-md-7'})
