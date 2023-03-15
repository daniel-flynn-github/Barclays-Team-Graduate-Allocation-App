from allauth.account.forms import ResetPasswordForm
from django.http import HttpRequest
from django.conf import settings
from allocationapp.models import *
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allocationapp.settings')


def reset_teams():
    teams = Team.objects.all()
    for team in teams:
        team.skills.all().delete()
        team.technologies.all().delete()
        team.delete()
    Department.objects.all().delete()


def reset_graduates_managers():
    graduates = Graduate.objects.all()
    managers = Manager.objects.all()
    if graduates:
        for graduates in graduates:
            temp_id = graduates.user.id
            graduates.delete()
            CustomUser.objects.filter(id=temp_id).delete()
    if managers:
        for manager in managers:
            temp_id = manager.user.id
            manager.delete()
            CustomUser.objects.filter(id=temp_id).delete()


def reset_users():
    CustomUser.objects.all().delete()


def send_password_reset(user: settings.AUTH_USER_MODEL):
    request = HttpRequest()
    request.user = user
    if settings.DEBUG:
        request.META['HTTP_HOST'] = '127.0.0.1:8000'
    else:
        # TEMPORARY filler url must be  changed to real link when website is hosted
        request.META['HTTP_HOST'] = 'www.mysite.com'

    form = ResetPasswordForm({"email": user.email})
    if form.is_valid():
        form.save(request)


def is_grad(current_user):
    try:
        Graduate.objects.get(user=CustomUser.objects.get(id=current_user.id))
        return True
    except:
        return False


def is_manager(current_user):
    try:
        Manager.objects.get(user=CustomUser.objects.get(id=current_user.id))
        return True
    except:
        return False


def is_admin(current_user):
    try:
        Admin.objects.get(user=CustomUser.objects.get(id=current_user.id))
        return True
    except:
        return False


def allocation_run():
    allocation_state = AllocationState.objects.first()
    if allocation_state:
        return allocation_state.has_allocated
    else:
        return False


def grad_has_already_voted(current_user):
    votes = Preference.objects.filter(graduate=Graduate.objects.get(user=CustomUser.objects.get(id=current_user.id)))
    return len(votes) > 0
