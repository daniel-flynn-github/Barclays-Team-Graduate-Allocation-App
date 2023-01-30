from django.test import TestCase
from .models import Graduate, Team, Preference, CustomUser
from django.test import Client
from django.urls import reverse
from . import allocation

class TestGetAllocation(TestCase):
    def setUp(self):
        grad1 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad1", email="grad1@barclays.com"))
        grad2 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad2", email="grad2@barclays.com"))
        grad3 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad3", email="grad3@barclays.com"))
        grad4 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad4", email="grad4@barclays.com"))
        grad5 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad5", email="grad5@barclays.com"))
        grad6 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad6", email="grad6@barclays.com"))
        grad7 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad7", email="grad7@barclays.com"))
        grad8 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad8", email="grad8@barclays.com"))
        grad9 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad9", email="grad9@barclays.com"))
        grad10 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad10", email="grad10@barclays.com"))

        team1 = Team.objects.create(name = "team1", capacity=3)
        team2 = Team.objects.create(name = "team2", capacity=4)
        team3 = Team.objects.create(name = "team3", capacity=5)

        

        # graduates = {
        #     grad1:{team1:100,team2:1,team3:3},
        #     grad2:{team1:1,team2:100,team3:5},
        #     grad3:{team1:2,team2:3,team3:100},
        #     grad4:{team1:100,team2:5,team3:2,},
        #     grad5:{team1:3,team2:100,team3:3},
        #     grad6:{team1:2,team2:3,team3:1},
        #     grad7:{team1:1,team2:2,team3:100},
        #     grad8:{team1:2,team2:100,team3:4}
        # }

        graduates = {
            'grad1':{'team1':100,'team2':1,'team3':3},
            'grad2':{'team1':1,'team2':100,'team3':5},
            'grad3':{'team1':2,'team2':3,'team3':100},
            'grad4':{'team1':100,'team2':5,'team3':2},
            'grad5':{'team1':3,'team2':100,'team3':3},
            'grad6':{'team1':100,'team2':3,'team3':1},
            'grad7':{'team1':1,'team2':2,'team3':100},
            'grad8':{'team1':2,'team2':100,'team3':4},
		    'grad9':{'team1':3,'team2':100,'team3':5},
		    'grad10':{'team1':5,'team2':1,'team3':100}
        }


        for grad,pref_list in graduates.items():
            for team,weight in pref_list.items():
                Preference.objects.create(grad=Graduate.objects.get(user=CustomUser.objects.get(first_name=grad)), 
                                        team = Team.objects.get(name=team),
                                        weight = weight)

          

    def test_get_allocation(self):
        c = Client()
        #logged_in = c.login(username='', password='')
        #self.assertTrue(logged_in)
        # response = c.get(reverse('allocationapp:get_allocation'))
        # print(response)
        self.assertEqual(len(list(Graduate.objects.all())), 10)
        self.assertEqual(len(list(Team.objects.all())), 3)
        self.assertEqual(Team.objects.get(name="team1").capacity, 3)
        self.assertEqual(Team.objects.get(name="team2").capacity, 4)
        self.assertEqual(Team.objects.get(name="team3").capacity, 5)
        self.assertEqual(len(allocation.allGraduates), 2)
        self.assertEqual(len(allocation.allTeams), 2)
        self.assertEqual(allocation.vacancies_on_lower_bound, 9)
        #self.assertEqual(allocation.total_vacancies, 12)
        response = allocation.run_allocation()
        print(response)
        #self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad4")).assigned_team, Team.objects.get(name="team3"))
        #self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad10")).assigned_team, Team.objects.get(name="team3"))
        # self.assertEqual(response.status_code, 200)
        # self.assertJSONEqual(
        #     str(response.content, encoding='utf8'),
        #     {
        #         "user":"pmccartney@beatles.com",
        #         "photo":"flinder/media/images/mountain.png",
        #         "name":"Thomas",
        #         "subtitle":"Mountain Flat"
        #     }
        # )
