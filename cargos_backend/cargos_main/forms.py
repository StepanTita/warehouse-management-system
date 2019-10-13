from django import forms


class NewCargoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)

    row = forms.IntegerField(label="Row")
    elevation = forms.IntegerField(label="Elevation")
    position = forms.IntegerField(label="Position")

    height = forms.DecimalField(decimal_places=2, max_digits=9)
    length = forms.DecimalField(decimal_places=2, max_digits=9)
    width = forms.DecimalField(decimal_places=2, max_digits=9)

    description = forms.CharField(label="Description", max_length=500, widget=forms.Textarea)

    title.widget.attrs.update({'class': 'col-md-12'})
    row.widget.attrs.update({'class': 'col-md-12'})
    elevation.widget.attrs.update({'class': 'col-md-12'})
    position.widget.attrs.update({'class': 'col-md-12'})
    height.widget.attrs.update({'class': 'col-md-12'})
    length.widget.attrs.update({'class': 'col-md-12'})
    width.widget.attrs.update({'class': 'col-md-12'})
    description.widget.attrs.update({'class': 'col-md-12'})
