from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .custom_decorators import check_graduate_status, check_admin_status
from .models import *
import json

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
