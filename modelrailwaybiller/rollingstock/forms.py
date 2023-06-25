from django import forms


class StockForm(forms.Form):
    road_name = forms.CharField(label="Reporting Mark:", max_length=4)
    id_number = forms.IntegerField(label="Registration Number")
    aar_type = forms.CharField(label="AAR Type:", max_length=2)
    cargo = forms.CharField(label="Cargo carried:", max_length=100)
    loaded = forms.BooleanField(label="Loaded?")
    location = forms.CharField(label="Current Location:")
