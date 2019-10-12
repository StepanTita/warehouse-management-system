from django import forms


class NewCargoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)

    cargo_ID = forms.IntegerField(label="ID")

    row = forms.IntegerField(label="Row")
    elevation = forms.IntegerField(label="Elevation")
    position = forms.IntegerField(label="Position")

    description = forms.CharField(label="Description", max_length=500, widget=forms.Textarea)
