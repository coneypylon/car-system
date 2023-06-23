from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RailUser
from layout.models import Layout
from django.db.models import Max


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    layout_id = forms.IntegerField(required=False)

    class Meta:
        model = RailUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2','layout_id')

    def clean_layout_id(self):
        layout_id = self.cleaned_data.get('layout_id')
        highest_layout_id = Layout.objects.aggregate(id__max=Max('id'))['id__max']
        if layout_id is None:
            layout_id = highest_layout_id + 1 if highest_layout_id else 1
        elif layout_id <= highest_layout_id:
            raise forms.ValidationError("Layout ID must be higher than existing layout IDs.")
        return layout_id