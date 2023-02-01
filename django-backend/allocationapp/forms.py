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
    gradId = forms.IntegerField()
    teamId = forms.IntegerField()
    weight = forms.IntegerField()

    class Meta:
        model = Preference
        fields = ['gradId', 'teamId', 'weight']

class GradCSVForm(forms.Form):
    csvfile = forms.FileField(
        label = 'Select a file',
        help_text = ''
    )

class TeamCSVForm(forms.Form):
    csvfile = forms.FileField(
        label = 'Select a file',
        help_text = ''
    )
