from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from allocationapp.models import Grad_CSV
from allocationapp.forms import GradCSVForm

def upload_file(request):
    if request.method == 'POST':
        form = GradCSVForm(request.POST, request.FILES)
        if form.is_valid():
            newcsv = Grad_CSV(csvfile = request.FILES['csvfile'])
            newcsv.save()
            return redirect(reverse('allocationapp:upload'))
    else:
        form = GradCSVForm
    all_csv = Grad_CSV.objects.all()
    return render(request, 'allocationapp/upload.html', {'form': form, 'all_csv': all_csv})


def index(request):
    return redirect(reverse('allocationapp:cast_votes'))

@login_required
def cast_votes(request):
    # Currently populated with mock data
    # Frontend expects this format.
    #   'teams' will be a list of dictionaries, each with the desired team info
    #   could also potentially have a Class GradTeam, and the 'teams' list will be a list of instances of GradTeam?
    #   will require minor frontend changes if this path is chosen.
    context_dict = {
        'teams': [
            {
                'team_name': 'Team 1',
                'department': 'Data Analytics',
                'technologies': ['Python', 'Java', 'Django'],
                'skills': ['Mathematics', 'Programming'],
                'group_size': 16,
                'description': 'description text here',
                'id': 123,  # unique ID
            },

            {
                'team_name': 'Team 2',
                'department': 'Banking Apps',
                'technologies': ['C++', 'Java', 'C#'],
                'skills': ['Smartness', 'Programming'],
                'group_size': 20,
                'description': 'description text here as well',
                'id': 345,
            }
        ]
    }

    return render(request, 'allocationapp/cast_votes.html', context=context_dict)

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
