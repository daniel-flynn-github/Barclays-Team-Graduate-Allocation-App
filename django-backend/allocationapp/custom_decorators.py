from .models import *


def check_graduate_status(current_user):
    try:
        Graduate.objects.get(user=CustomUser.objects.get(id=current_user.id))
        return True
    except:
        return False


def check_manager_status(current_user):
    try:
        Manager.objects.get(user=CustomUser.objects.get(id=current_user.id))
        return True
    except:
        return False


def check_admin_status(current_user):
    try:
        Admin.objects.get(user=CustomUser.objects.get(id=current_user.id))
        return True
    except:
        return False
