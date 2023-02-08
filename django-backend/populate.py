import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allocationapp.settings')

import django
from random import randint
django.setup()

from allocationapp.models import *

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


def add_user(user_dict):
    user = CustomUser.objects.create(username=user_dict.get('username'), email=user_dict.get('email'))
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

if __name__ == "__main__":
    populate()
