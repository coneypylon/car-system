from django import forms
from .models import RailVehicle


class StockForm(forms.ModelForm):
    '''
    road_name = forms.CharField(label="Reporting Mark:", max_length=4)
    id_number = forms.IntegerField(label="Registration Number")
    aar_type = forms.CharField(label="AAR Type:", max_length=2)
    cargo = forms.CharField(label="Cargo carried:", max_length=100)
    loaded = forms.BooleanField(label="Loaded?")
    location = forms.CharField(label="Current Location:")
    '''
    class Meta:
        model = RailVehicle
        exclude = ['location_str', 'last_loaded_unloaded','ready_for_pickup']

class ConfirmationForm(forms.Form):
    registration = forms.CharField(label="Confirm car registration (e.g. CNWX123456):", max_length=10)
