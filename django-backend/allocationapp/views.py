from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from .allocation import run_allocation
from .models import *
from .forms import CSVForm
from .utilities import *

import json
import csv


@login_required
def index(request):
    # After user tries to access a page they aren't allowed to access,
    # they get redirected here and then further redirected to their correct page.
    if is_manager(request.user):
        return redirect(reverse('allocationapp:manager_view_teams'))
    elif is_grad(request.user):
        return redirect(reverse('allocationapp:cast_votes'))
    elif is_admin(request.user):
        return redirect(reverse('allocationapp:portal'))
    else:
        # You're logged in as the superuser, to avoid issues, we log you out so you can login with a webapp account.
        logout(request)
        return redirect(reverse('allocationapp:index'))


#  ---- Begin GRADUATE views ----
@login_required
@user_passes_test(is_grad, login_url='/allocation/')
def cast_votes(request):
    current_user = request.user
    if request.method == "POST":
        # If this graduate has already cast their votes, instead of creating a set of new records, we
        # delete their old ones first.
        Preference.objects.filter(graduate=Graduate.objects.get(
            user=CustomUser.objects.get(id=current_user.id))).delete()

        votes = json.loads(request.POST.get('votes'))

        for team_id in votes:
            p = Preference(
                team=Team.objects.get(id=int(team_id)),
                weight=votes[team_id],
                graduate=Graduate.objects.get(
                    user=CustomUser.objects.get(id=current_user.id))
            )
            p.save()

        return redirect(reverse('allocationapp:vote_submitted'))
    else:
        context_dict = {
            'teams': Team.objects.all(),
        }

        return render(request, 'allocationapp/cast_votes.html', context=context_dict)


@login_required
@user_passes_test(is_grad, login_url='/allocation/')
def vote_submitted(request):
    current_graduate = Graduate.objects.filter(user=CustomUser.objects.get(id=request.user.id)).first()
    context_dict = {
        'current_graduate': current_graduate,
        'assigned_team': current_graduate.assigned_team,
    }
    return render(request, 'allocationapp/vote_submitted.html', context=context_dict)


@login_required
@user_passes_test(is_grad, login_url='/allocation/')
def result_page(request):
    current_user = Graduate.objects.get(user=CustomUser.objects.get(id=request.user.id))
    context_dict = {
        'assigned_team': current_user.assigned_team,
        'assigned_team_members': Graduate.objects.filter(
            assigned_team=Team.objects.get(id=current_user.assigned_team.id)),
        'current_user_id': request.user.id,
        'assigned_team_members': Graduate.objects.filter(
            assigned_team=Team.objects.get(id=current_user.assigned_team.id)),
        'current_user_id': request.user.id,
    }

    return render(request, 'allocationapp/result_page.html', context=context_dict)


# ---- Begin MANAGER views ----
@login_required
@user_passes_test(is_manager, login_url='/allocation/')
def manager_view_teams(request):
    # Similar to the cast votes page -- a manager can view all of their team(s) here
    # and edit them as needed. This is essentially the managers "Homepage"
    if request.method == "GET":
        teams = Team.objects.filter(manager=Manager.objects.get(
            user=CustomUser.objects.get(id=request.user.id)))
        team_members = {}

        for team in teams:
            team_members[team.id] = Graduate.objects.filter(
                assigned_team=Team.objects.get(id=team.id))

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
@user_passes_test(is_manager, login_url='/allocation/')
def delete_team_member(request, user_id):
    Graduate.objects.filter(user=CustomUser.objects.get(
        id=user_id)).update(assigned_team=None)
    response_data = {'success': True}
    return JsonResponse(response_data)

@login_required
@user_passes_test(is_manager, login_url='/allocation/')
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

            for technology in technologies:
                team.technologies.add(int(technology))

        return redirect(reverse('allocationapp:manager_view_teams'))

    else:
        return render(request, 'allocationapp/edit_team.html', context=context_dict)


# ---- Begin ADMIN views ----
@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def upload_file(request):
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        print("posted")
        if form.is_valid():
            print("valid")
            if UserCSV.objects.all().count() > 0:
                UserCSV.objects.all().delete()
            new_csv = UserCSV(csv_file=request.FILES['csv_file'], pk=1)
            new_csv.save()
            return redirect(reverse('allocationapp:upload'))
    else:
        form = CSVForm
    all_csv = UserCSV.objects.all()
    return render(request, 'allocationapp/upload.html', {'form': form, 'all_csv': all_csv, 'populated': False})


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def populate_db(request):
    reset_graduates_managers()
    csv_file = UserCSV.objects.get(pk=1).csv_file
    path = csv_file.path
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            new_user, created = CustomUser.objects.get_or_create(
                first_name=row[0],
                last_name=row[1],
                email=row[2],
                password=make_password(
                    CustomUser.objects.make_random_password())
            )
            if row[3] == 'graduate':
                Graduate.objects.get_or_create(
                    user=new_user
                )
            if row[3] == 'manager':
                Manager.objects.get_or_create(
                    user=new_user
                )
            send_password_reset(new_user)
    allcsv = UserCSV.objects.all()
    form = CSVForm()
    return render(request, 'allocationapp/upload.html', {'populated': True, 'all_csv': allcsv, 'form': form})


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def team_upload_file(request):
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            if TeamCSV.objects.all().count() > 0:
                TeamCSV.objects.all().delete()
            new_csv = TeamCSV(csv_file=request.FILES['csv_file'], pk=1)
            new_csv.save()
            return redirect(reverse('allocationapp:team_upload'))
    else:
        form = CSVForm
    all_csv = TeamCSV.objects.all()
    return render(request, 'allocationapp/team_upload.html', {'form': form, 'all_csv': all_csv, 'populated': False})


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def team_populate_db(request):
    reset_teams()
    csv_file = TeamCSV.objects.get(pk=1).csv_file
    path = csv_file.path
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            department, created = Department.objects.get_or_create(
                name=row[3]
            )
            manager_user = CustomUser.objects.get(email=row[4])
            new_team, created = Team.objects.get_or_create(
                name=row[0],
                description=row[1],
                capacity=row[2],
                department=department,
                manager=Manager.objects.get(user_id=manager_user.id)
            )
            technologies = row[5].split(',')
            for technology in technologies:
                technology = technology.strip()
                technology_instance, created = Technology.objects.get_or_create(
                    name=technology)
                new_team.technologies.add(technology_instance)
            skills = row[6].split(',')
            for skill in skills:
                skill = skill.strip()
                skill_instance, created = Skill.objects.get_or_create(
                    name=skill)
                new_team.skills.add(skill_instance)

    graduates = Graduate.objects.all()
    teams = Team.objects.all()
    for graduate in graduates:
        for team in teams:
            Preference.objects.get_or_create(
                graduate=graduate, team=team, weight=5)
    allcsv = TeamCSV.objects.all()
    form = CSVForm()
    return render(request, 'allocationapp/team_upload.html', {'populated': True, 'all_csv': allcsv, 'form': form})


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def reset_teams_view(request):
    reset_teams()
    form = CSVForm
    return render(request, 'allocationapp/team_upload.html', {'populated': False, 'allcsv': '', 'form': form})


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def reset_graduates_managers_view(request):
    reset_graduates_managers()
    form = CSVForm
    return render(request, 'allocationapp/upload.html', {'populated': False, 'allcsv': '', 'form': form})


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def get_allocation(request):
    # Run alg
    run_allocation(list(Graduate.objects.all()), list(Team.objects.all()))
    # redirect to result page
    return redirect(reverse('allocationapp:allocation_already_run'))


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def create_new_team(request):
    if request.method == 'POST':
        name = request.POST['group_name']
        manager = request.POST['group_manager']
        department_id = request.POST['group_department']
        department_input = request.POST['department_input']
        technologies = request.POST['group_technologies']
        skills = request.POST['group_skills']
        capacity = request.POST['group_capacity']
        description = request.POST['group_description']

        team_info, created = Team.objects.get_or_create(name=name,
                                                        capacity=int(capacity),
                                                        description=description,
                                                        manager=Manager.objects.get(id=int(manager)))

        if department_id == 'other':
            Department.objects.get_or_create(name=department_input)
            team_info.department = Department.objects.get(name=department_input)
        else:
            team_info.department = Department.objects.get(id=int(department_id))

        skill_split = skills.split(',')
        tech_spilt = technologies.split(",")
        for skill in skill_split:
            skill_info, created = Skill.objects.get_or_create(name=skill)
            team_info.skills.add(Skill.objects.get(name=skill_info))
        for technology in tech_spilt:
            tech_info, created = Technology.objects.get_or_create(name=technology)
            team_info.technologies.add(Technology.objects.get(name=tech_info))

        team_info.save()
        return redirect(reverse('allocationapp:manager_view_teams'))
    departments = Department.objects.all()
    skills = Skill.objects.all()
    technologies = Technology.objects.all()
    managers = Manager.objects.all()
    context_dict = {'managers': managers, 'departments': departments, 'skills': skills, 'technologies': technologies,
                    'count': range(0, 200)}
    return render(request, 'allocationapp/create_new_team.html', context=context_dict)


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def create_new_grad(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        role_id = int(request.POST['role'])

        new_user, created = CustomUser.objects.get_or_create(first_name=first_name,
                                                             last_name=last_name,
                                                             email=email,
                                                             password=make_password(
                                                                 CustomUser.objects.make_random_password())
                                                             )
        if role_id == 1:
            Manager.objects.get_or_create(user=new_user)
        if role_id == 2:
            Graduate.objects.get_or_create(user=new_user)
        send_password_reset(new_user)
        return redirect(reverse('allocationapp:upload'))

    return render(request, 'allocationapp/create_new_graduate.html')


@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def admin_portal(request):
    return render(request, 'allocationapp/admin_portal.html')

@login_required
@user_passes_test(is_admin, login_url='/allocation/')
def allocation_already_run(request):
    return render(request, 'allocationapp/allocation_already_run.html')