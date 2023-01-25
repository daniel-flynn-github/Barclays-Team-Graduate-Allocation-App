from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .custom_decorators import *
from .models import *
import json

def index(request):
    return redirect(reverse('allocationapp:cast_votes'))

@login_required
def manager_view_teams(request):
    # Similar to the cast votes page -- a manager can view all of their team(s) here
    # and edit them as needed. This is essentially the managers "Homepage"
    if request.method == "GET":
        if not (check_manager_status(request.user)):
            # Redirect if the user is not a MANAGER.
            return redirect(reverse('allocationapp:index'))
        
        teams = Team.objects.filter(manager=Manager.objects.get(user=CustomUser.objects.get(id=request.user.id)))
        team_members = {}

        for team in teams:
            team_members[team.id] = Graduate.objects.filter(assigned_team=Team.objects.get(id=team.id))

        context_dict = {
            'teams': teams,
            'team_members': team_members,
        }

        return render(request, 'allocationapp/manager_teams.html', context=context_dict)

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
            return redirect(reverse('allocationapp:manager_view_teams'))

        context_dict = {
            'teams': Team.objects.all()
        }

        return render(request, 'allocationapp/cast_votes.html', context=context_dict)

@login_required
def vote_submitted(request):
    if not (check_graduate_status(request.user)):
        # Redirect if the user is not a GRADUATE.
        return redirect(reverse('allocationapp:manager_view_teams'))

    context_dict = {}
    return render(request, 'allocationapp/vote_submitted.html', context=context_dict)

@login_required
def result_page(request):
    if not (check_graduate_status(request.user)):
        # Redirect if the user is not a GRADUATE.
        return redirect(reverse('allocationapp:manager_view_teams'))

    current_user = Graduate.objects.get(user=CustomUser.objects.get(id=request.user.id))
    context_dict = {
        'assigned_team': current_user.assigned_team,
        'assigned_team_members': Graduate.objects.filter(assigned_team=Team.objects.get(id=current_user.assigned_team.id)),
        'current_user_id': request.user.id
    }

    return render(request, 'allocationapp/result_page.html', context=context_dict)
