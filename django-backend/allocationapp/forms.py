from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Preference


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class PreferencesForm(forms.Form):
    grad_ID = forms.IntegerField()
    team_ID = forms.IntegerField()
    weight = forms.IntegerField()

    class Meta:
        model = Preference
        fields = ['gradId', 'teamId', 'weight']


class CSVForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a file',
        help_text=''
    )
