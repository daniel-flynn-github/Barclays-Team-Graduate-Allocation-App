from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Admin
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Preference)
admin.site.register(Team)
admin.site.register(Graduate)
admin.site.register(Manager)
admin.site.register(Skill)
admin.site.register(Technology)
admin.site.register(Admin)