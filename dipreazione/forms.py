from django import forms

class CreateMeatingForm(forms.Form):
    name = forms.CharField(max_length=200)

