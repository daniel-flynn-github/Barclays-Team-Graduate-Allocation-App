from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Preference, Team


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

class TeamForm(forms.ModelForm):
    name = forms.CharField()
    capacity = forms.IntegerField()
    department = forms.CharField()
    skills = forms.CharField()
    technologies = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Team
        fields = ['name', 'capacity', 'department', 'skills', 'technologies', 'description']

