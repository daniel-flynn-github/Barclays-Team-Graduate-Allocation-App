from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .custom_decorators import check_graduate_status, check_admin_status
from .models import *
import json
import csv

#from allocationapp.models import Grad_CSV, Graduate, Manager
from allocationapp.forms import GradCSVForm
from django.contrib.auth.models import AbstractUser

def upload_file(request):
    if request.method == 'POST':
        form = GradCSVForm(request.POST, request.FILES)
        if form.is_valid():
            if Grad_CSV.objects.all().count() > 0:
                Grad_CSV.objects.all().delete()
            newcsv = Grad_CSV(csvfile = request.FILES['csvfile'], pk = 1)
            newcsv.save()
            return redirect(reverse('allocationapp:upload'))
    else:
        form = GradCSVForm
    all_csv = Grad_CSV.objects.all()
    return render(request, 'allocationapp/upload.html', {'form': form, 'all_csv': all_csv, 'populated' : False})

def populate_db(request):
    rs()
    csv_file = Grad_CSV.objects.get(pk=1).csvfile
    path = csv_file.path
    print(type(path))
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            new_user, created = CustomUser.objects.get_or_create(
                first_name = row[0],
                last_name = row[1],
                email = row[2],
                password = make_password(CustomUser.objects.make_random_password())
            )
            if row[3] == 'graduate':
                Graduate.objects.get_or_create(
                    user = new_user
                )
            if row[3] == 'manager':
                Manager.objects.get_or_create(
                    user=new_user
                )
    allcsv = Grad_CSV.objects.all()
    form = GradCSVForm()
    return render(request,'allocationapp/upload.html', {'populated' : True, 'all_csv': allcsv, 'form' : form})

def rs():
    grads = Graduate.objects.all()
    managers  = Manager.objects.all()
    if grads:
        for grad in grads:
            CustomUser.objects.get(id = grad.user_id).delete()
    if managers:
        for manager in managers:
            CustomUser.objects.get(id = manager.user_id).delete()


def reset(request):
    rs()
    Grad_CSV.objects.all().delete()
    form = GradCSVForm
    return render(request,'allocationapp/upload.html', {'populated' : False, 'allcsv': '', 'form' : form})

def index(request):
    return redirect(reverse('allocationapp:index'))

@login_required
def cast_votes(request):
    if request.method == "POST":
        votes = json.loads(request.POST.get('votes'))
        current_user = request.user
        
        for team_id in votes:
            p = Preference(
                    team=Team.objects.get(id=int(team_id)), 
                    weight=votes[team_id], 
                    grad=Graduate.objects.get(user=CustomUser.objects.get(id=current_user.id))
                )
            p.save()

        return redirect(reverse('allocationapp:vote_submitted'))
    else:

        if not (check_graduate_status(request.user)):
            # Redirect if the user is not a GRADUATE.
            return redirect(reverse('allocationapp:index'))

        context_dict = {
            'teams': Team.objects.all()
        }

        return render(request, 'allocationapp/cast_votes.html', context=context_dict)

@login_required
def vote_submitted(request):
    if not (check_graduate_status(request.user)):
        # Redirect if the user is not a GRADUATE.
        return redirect(reverse('allocationapp:index'))

    context_dict = {}
    return render(request, 'allocationapp/vote_submitted.html', context=context_dict)

@login_required
def result_page(request):
    if not (check_graduate_status(request.user)):
        # Redirect if the user is not a GRADUATE.
        return redirect(reverse('allocationapp:index'))

    current_user = Graduate.objects.get(user=CustomUser.objects.get(id=request.user.id))
    context_dict = {
        'assigned_team': current_user.assigned_team,
        'assigned_team_members': Graduate.objects.filter(assigned_team=Team.objects.get(id=current_user.assigned_team.id)),
        'current_user_id': request.user.id
    }

    return render(request, 'allocationapp/result_page.html', context=context_dict)
