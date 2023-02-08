import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
from random import randint
django.setup()

from allocationapp.models import CustomUser, Manager, Team, Graduate, Admin, Preference

def populate():
    users = [
        {'username' = 'user1', 'email' = 'user1@email.com'},
        {'username' = 'user2', 'email' = 'user2@email.com'},
        {'username' = 'user3', 'email' = 'user3@email.com'},
        {'username' = 'user4', 'email' = 'user4@email.com'},
        {'username' = 'user5', 'email' = 'user5@email.com'},
        {'username' = 'user6', 'email' = 'user6@email.com'},
        {'username' = 'user7', 'email' = 'user7@email.com'},
        {'username' = 'user8', 'email' = 'user8@email.com'},
        {'username' = 'user9', 'email' = 'user9@email.com'},
        {'username' = 'user10', 'email' = 'user10@email.com'},
        {'username' = 'user11', 'email' = 'user11@email.com'},
        {'username' = 'user12', 'email' = 'user12@email.com'},
        {'username' = 'user13', 'email' = 'user13@email.com'},
        {'username' = 'user14', 'email' = 'user14@email.com'},
        {'username' = 'user15', 'email' = 'user15@email.com'}
        {'username' = 'user16', 'email' = 'user16@email.com'}
    ]

    teams = [
        {'name' = 'team1', 'description' = 'this is team 1', 'capacity' = 5}
        {'name' = 'team2', 'description' = 'this is team 2', 'capacity' = 6}
        {'name' = 'team3', 'description' = 'this is team 3', 'capacity' = 2}
        {'name' = 'team4', 'description' = 'this is team 4', 'capacity' = 7}
    ]

    for user in users:
        u = CustomerUser.objects.get_or_create(username = user['username'], email = user['email'])
        if user['username'] == 'user1' or 'user5' or 'user10' or 'user15':
            Manager.objects.get_or_create(user = u)
        if user['username'] == 'user16':
            Admin.objects.get_or_create(user = u)
        else:
            Graduate.objects.get_or_create(user = u)

    for team in teams:
        t = Team.objects.get_or_create(name = team['name'], description = team['description'], capacity = team['capacity'])

    grads = Graduate.objects.all()
    teams = Team.objects.all()
    Managers = 
    slice = len(grads)/len(teams)
    for grad in grads:




