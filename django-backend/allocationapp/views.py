from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Team, CustomUser, Department, Preference
from .forms import PreferencesForm
import json

def index(request):
    return redirect(reverse('allocationapp:cast_votes'))

@login_required
def cast_votes(request):
    if request.method == "GET":
        context_dict = {
            'teams': Team.objects.all()
        }

        return render(request, 'allocationapp/cast_votes.html', context=context_dict)
    else:
        votes = json.loads(request.POST.get('votes'))
        
        for team_id in votes:
            p = Preference(teamId=Team.objects.get(id=int(team_id)), weight=votes[team_id], gradId=CustomUser.objects.get(id=7))
            p.save()

        return redirect(reverse('allocationapp:cast_votes'))

@login_required
def vote_submitted(request):
    context_dict = {}
    return render(request, 'allocationapp/vote_submitted.html', context=context_dict)

@login_required
def result_page(request):
    context_dict = {
        'teams': [
            {
                'team_name': 'Team 1',
                'group_size': 16,
                'manage_name': 'Casey',
                'team_members'
                'id': 123,  # unique ID
            },
        ],
        'students':[
            {
                'student_name' : 'student1',
                'student_id' : '1',
                'group_id' : 123,
            },
            {
                'student_name': 'student2',
                'student_id': '2',
                'group_id': 123,
            },
            {
                'student_name': 'student3',
                'student_id': '3',
                'group_id': 123,
            },
        ]
    }
    return render(request, 'allocationapp/result_page.html', context=context_dict)
