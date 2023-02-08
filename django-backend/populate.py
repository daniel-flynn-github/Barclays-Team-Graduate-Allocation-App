import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allocationproject.settings')

import django
django.setup()

from allocationapp.models import *
from django.contrib.auth.hashers import make_password
import random

def populate():
    users = [
        # Create all the grads (12)
        {'username': 'grad1', 'email': 'grad1@email.com', 'level': 'graduate'},
        {'username': 'grad2', 'email': 'grad2@email.com', 'level': 'graduate'},
        {'username': 'grad3', 'email': 'grad3@email.com', 'level': 'graduate'},
        {'username': 'grad4', 'email': 'grad4@email.com', 'level': 'graduate'},
        {'username': 'grad5', 'email': 'grad5@email.com', 'level': 'graduate'},
        {'username': 'grad6', 'email': 'grad6@email.com', 'level': 'graduate'},
        {'username': 'grad7', 'email': 'grad7@email.com', 'level': 'graduate'},
        {'username': 'grad8', 'email': 'grad8@email.com', 'level': 'graduate'},
        {'username': 'grad9', 'email': 'grad9@email.com', 'level': 'graduate'},
        {'username': 'grad10', 'email': 'grad10@email.com', 'level': 'graduate'},
        {'username': 'grad11', 'email': 'grad11@email.com', 'level': 'graduate'},
        {'username': 'grad12', 'email': 'grad12@email.com', 'level': 'graduate'},

        # Create all the managers (3)
        {'username': 'manager1', 'email': 'manager1@email.com', 'level': 'manager'},
        {'username': 'manager2', 'email': 'manager2@email.com', 'level': 'manager'},
        {'username': 'manager3', 'email': 'manager3@email.com', 'level': 'manager'},

        # Create an admin
        {'username': 'admin', 'email': 'admin@email.com', 'level': 'admin'},
    ]

    departments = [
        {'name': 'Data Analytics'},
        {'name': 'Banking Security'},
        {'name': 'Business Banking'},
    ]

    skills = [
        {'name': 'Data Science'},
        {'name': 'Mathematics'},
        {'name': 'Programming'},
        {'name': 'Critical Thinking'},
    ]

    technologies = [
        {'name': 'Python'},
        {'name': 'Java'},
        {'name': 'C/C++'},
        {'name': 'GoLang'},
    ]

    teams = [
        {
            'name': 'Barclays Div 1',
            'description': 'This is a team!',
            'capacity': 16,
            'department': 'Data Analytics',
            'manager': 'manager1',
            'lower_bound': 1,
        },
        {
            'name': 'Barclays Div 2',
            'description': 'This is a team!',
            'capacity': 20,
            'department': 'Data Analytics',
            'manager': 'manager2',
            'lower_bound': 1,
        },
        {
            'name': 'Barclays Div 3',
            'description': 'This is a team!',
            'capacity': 8,
            'department': 'Banking Security',
            'manager': 'manager3',
            'lower_bound': 1,
        },
        {
            'name': 'Barclays Div 4',
            'description': 'This is a team!',
            'capacity': 14,
            'department': 'Business Banking',
            'manager': 'manager3',
            'lower_bound': 1,
        },
    ]

    for user in users:
        add_user(user)

    for department in departments:
        add_department(department)

    for skill in skills:
        add_skill(skill)

    for technology in technologies:
        add_technology(technology)

    for team in teams:
        add_team(team, skills, technologies)

    cast_mock_preferences()


def add_user(user_dict):
    first_names = ['Luke', 'Gianmarco', 'Daniel', 'Yuqi', 'Alaa']
    last_names = ['Smith', 'McKay', 'Johnstone', 'Hans', 'White']

    user = CustomUser.objects.create(
        username=user_dict.get('username'), 
        email=user_dict.get('email'), 
        password=make_password('testing_1'),
        first_name=random.choice(first_names),
        last_name=random.choice(last_names)
    )
    status = user_dict.get('level')

    if status == 'graduate':
        Graduate.objects.create(user=user)
    elif status == 'manager':
        Manager.objects.create(user=user)
    else:
        Admin.objects.create(user=user)

def add_department(department_dict):
    Department.objects.create(name=department_dict.get('name'))

def add_skill(skill_dict):
    Skill.objects.create(name=skill_dict.get('name'))

def add_technology(technology_dict):
    Technology.objects.create(name=technology_dict.get('name'))

def add_team(team_dict, skills, technologies):
    # Assign the static parameters.
    added_team = Team.objects.create(
        name=team_dict.get('name'),
        description=team_dict.get('description'),
        capacity=team_dict.get('capacity'),
        lower_bound=team_dict.get('lower_bound'),
    )

    # Find the department and manager to assign them.
    added_team.department = Department.objects.get(name=team_dict.get('department'))
    added_team.manager = Manager.objects.get(user=CustomUser.objects.get(username=team_dict.get('manager')))
    added_team.save()
    
    # Choose 2 random skills and technologies for each team.
    chosen_skills = random.sample(skills, 2)
    chosen_technologies = random.sample(technologies, 2)

    for i in range(2):
        added_team.skills.add(Skill.objects.get(name=chosen_skills[i].get('name')))
        added_team.technologies.add(Technology.objects.get(name=chosen_technologies[i].get('name')))

def cast_mock_preferences():
    teams = Team.objects.all()
    graduates = Graduate.objects.all()

    for graduate in graduates:
        for team in teams:
            Preference.objects.create(grad=graduate, team=team, weight=random.randint(0, 5))

if __name__ == "__main__":
    populate()
