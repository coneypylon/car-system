from django import forms
from .models import Layout, Location

class LayoutForm(forms.ModelForm):
    class Meta:
        model = Layout
        exclude = ["id","locations"]

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ["macro_location"]