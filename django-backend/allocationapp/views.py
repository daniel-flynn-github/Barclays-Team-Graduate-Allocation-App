from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .custom_decorators import *
from django.contrib.auth.hashers import make_password
from .allocation import run_allocation
from allauth.account.forms import ResetPasswordForm
from django.conf import settings
from django.http import HttpRequest
from .models import *
from .forms import GradCSVForm,TeamCSVForm

import json
import csv

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
    delete_grad_and_manager()
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
            send_password_reset(new_user)
    allcsv = Grad_CSV.objects.all()
    form = GradCSVForm()
    return render(request,'allocationapp/upload.html', {'populated' : True, 'all_csv': allcsv, 'form' : form})

def team_upload_file(request):
    if request.method == 'POST':
        form = TeamCSVForm(request.POST, request.FILES)
        if form.is_valid():
            if TeamCSV.objects.all().count() > 0:
                TeamCSV.objects.all().delete()
            newcsv = TeamCSV(csvfile = request.FILES['csvfile'], pk = 1)
            newcsv.save()
            return redirect(reverse('allocationapp:teamupload'))
    else:
        form = TeamCSVForm
    all_csv = TeamCSV.objects.all()
    return render(request, 'allocationapp/teamupload.html', {'form': form, 'all_csv': all_csv, 'populated' : False})

def team_populate_db(request):
    TeamCSV
    csv_file = TeamCSV.objects.get(pk=1).csvfile
    path = csv_file.path
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            dep, created = Department.objects.get_or_create(
                name = row[3]
            )
            manager_user = CustomUser.objects.get(email = row[4])
            new_team, created = Team.objects.get_or_create(
                name = row[0],
                description = row[1],
                capacity = row[2],
                department = dep,
                manager = Manager.objects.get(user_id = manager_user.id)
            )
    grads = Graduate.objects.all()
    teams = Team.objects.all()
    for grad in grads:
        for team in teams:
            Preference.objects.get_or_create(grad = grad, team = team, weight = 5)
    allcsv = TeamCSV.objects.all()
    form = TeamCSVForm()
    return render(request,'allocationapp/teamupload.html', {'populated' : True, 'all_csv': allcsv, 'form' : form})

def team_reset(request):
    Department.objects.all().delete()
    form = TeamCSVForm
    return render(request,'allocationapp/teamupload.html', {'populated' : False, 'allcsv': '', 'form' : form})

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

#utility function to delete graduate and manager objects
def delete_grad_and_manager():
    grads = Graduate.objects.all()
    managers  = Manager.objects.all()
    if grads:
        for grad in grads:
            temp_id = grad.user.id
            grad.delete()
            CustomUser.objects.filter(id = temp_id).delete()
    if managers:
        for manager in managers:
            temp_id = manager.user.id
            manager.delete()
            CustomUser.objects.filter(id = temp_id).delete()

def reset(request):
    delete_grad_and_manager()
    form = GradCSVForm
    return render(request,'allocationapp/upload.html', {'populated' : False, 'allcsv': '', 'form' : form})

def index(request):
    return redirect(reverse('allocationapp:cast_votes'))

@login_required
def manager_view_teams(request):
    # Similar to the cast votes page -- a manager can view all of their team(s) here
    # and edit them as needed. This is essentially the managers "Homepage"
    if request.method == "GET":
        teams = Team.objects.filter(manager=Manager.objects.get(user=CustomUser.objects.get(id=request.user.id)))
        team_members = {}

        for team in teams:
            team_members[team.id] = Graduate.objects.filter(assigned_team=Team.objects.get(id=team.id))

        context_dict = {
            'teams': teams,
            'team_members': team_members,
            'graduates_with_no_team': Graduate.objects.filter(assigned_team=None),
        }

        return render(request, 'allocationapp/manager_teams.html', context=context_dict)

    else:
        selected_grad_id = request.POST['selected_grad']
        team_id = request.POST['team_id']

        Graduate.objects.filter(user=CustomUser.objects.get(id=int(selected_grad_id))).update(
            assigned_team=Team.objects.get(id=int(team_id))
        )

        return redirect(reverse('allocationapp:manager_view_teams'))

@login_required
def delete_team_member(request, user_id):
    Graduate.objects.filter(user=CustomUser.objects.get(id=user_id)).update(assigned_team=None)
    return redirect(reverse('allocationapp:manager_view_teams'))

@login_required
def manager_edit_team(request, team_id):
    context_dict = {
        'team': Team.objects.get(id=team_id),
        'departments': Department.objects.all(),
        'technologies': Technology.objects.all(),
        'skills': Skill.objects.all(),
    }

    if request.method == 'POST':
        department_id = request.POST['department_id']
        technologies = request.POST.getlist('chosen_technologies')
        skills = request.POST.getlist('chosen_skills')
        capacity = request.POST['chosen_capacity']
        description = request.POST['chosen_description']

        teams = Team.objects.filter(id=team_id)
        teams.update(
            department=Department.objects.get(id=int(department_id)),
            capacity=int(capacity),
            description=description,
        )

        for team in teams:
            team.technologies.clear()
            team.skills.clear()

            for skill in skills:
                team.skills.add(int(skill))

            for tech in technologies:
                team.technologies.add(int(tech))

        return redirect(reverse('allocationapp:manager_view_teams')) 

    else:
        return render(request, 'allocationapp/edit_team.html', context=context_dict)

@login_required
def cast_votes(request):
    current_user = request.user
    if request.method == "POST":
        # If this grad has already cast their votes, instead of creating a set of new records, we
        # delete their old ones first.
        Preference.objects.filter(grad=Graduate.objects.get(user=CustomUser.objects.get(id=current_user.id))).delete()

        votes = json.loads(request.POST.get('votes'))
        
        for team_id in votes:
            p = Preference(
                    team=Team.objects.get(id=int(team_id)), 
                    weight=votes[team_id], 
                    grad=Graduate.objects.get(user=CustomUser.objects.get(id=current_user.id))
                )
            p.save()

        return redirect(reverse('allocationapp:vote_submitted'))
    else:
        context_dict = {
            'teams': Team.objects.all(),
        }

        return render(request, 'allocationapp/cast_votes.html', context=context_dict)

@login_required
def vote_submitted(request):
    current_user = request.user
    context_dict = {
        'current_grad': Graduate.objects.filter(user=CustomUser.objects.get(id=current_user.id)).first(),
    }
    return render(request, 'allocationapp/vote_submitted.html', context=context_dict)

@login_required
def result_page(request):
    current_user = Graduate.objects.get(user=CustomUser.objects.get(id=request.user.id))
    context_dict = {
        'assigned_team': current_user.assigned_team,
        'assigned_team_members': Graduate.objects.filter(assigned_team=Team.objects.get(id=current_user.assigned_team.id)),
        'current_user_id': request.user.id,
    }

    return render(request, 'allocationapp/result_page.html', context=context_dict)

@login_required
def get_allocation(request):
    # Run alg
    run_allocation(list(Graduate.objects.all()), list(Team.objects.all()))
    # redirect to result page
    return redirect(reverse('allocationapp:result_page'))
