from django import forms


class StockForm(forms.Form):
    road_name = forms.CharField(label="Road Name:", max_length=100)