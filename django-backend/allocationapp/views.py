from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .custom_decorators import *
from django.contrib.auth.hashers import make_password
from .custom_decorators import check_graduate_status, check_admin_status
from . import allocation
from .models import *
from .forms import GradCSVForm

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
            CustomUser.objects.get(id = grad.user.id).delete()
    if managers:
        for manager in managers:
            CustomUser.objects.get(id = manager.user.id).delete()

def reset(request):
    rs()
    Grad_CSV.objects.all().delete()
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
    if request.method == "POST":
        current_user = request.user

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
            'teams': Team.objects.all()
        }

        return render(request, 'allocationapp/cast_votes.html', context=context_dict)

@login_required
def vote_submitted(request):
    context_dict = {}
    return render(request, 'allocationapp/vote_submitted.html', context=context_dict)

@login_required
def result_page(request):
    current_user = Graduate.objects.get(user=CustomUser.objects.get(id=request.user.id))
    context_dict = {
        'assigned_team': current_user.assigned_team,
        'assigned_team_members': Graduate.objects.filter(assigned_team=Team.objects.get(id=current_user.assigned_team.id)),
        'current_user_id': request.user.id
    }

    return render(request, 'allocationapp/result_page.html', context=context_dict)

@login_required
def get_allocation(request):
    # Run alg
    allocation_results = allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()))
    # redirect to result page
    return redirect(reverse('allocationapp:result_page'))
