from django.test import TestCase
from .models import Graduate, Team, Preference, CustomUser
from django.test import Client
from django.urls import reverse
from . import allocation

class TestGetAllocation(TestCase):
    def setUp(self):
        team1 = Team.objects.create(name = "team1", capacity=3, lower_bound=2)
        team2 = Team.objects.create(name = "team2", capacity=4, lower_bound=3)
        team3 = Team.objects.create(name = "team3", capacity=5, lower_bound=4)

        # grad1 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad1", email="grad1@barclays.com"))
        # grad2 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad2", email="grad2@barclays.com"))
        # grad3 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad3", email="grad3@barclays.com"))
        # grad4 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad4", email="grad4@barclays.com"))
        # grad5 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad5", email="grad5@barclays.com"))
        # grad6 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad6", email="grad6@barclays.com"))
        # grad7 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad7", email="grad7@barclays.com"))
        # grad8 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad8", email="grad8@barclays.com"))
        # grad9 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad9", email="grad9@barclays.com"))
        # grad10 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad10", email="grad10@barclays.com"))
        grad1 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad1", email="grad1@barclays.com"), assigned_team=Team.objects.get(name="team1"))
        grad2 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad2", email="grad2@barclays.com"), assigned_team=Team.objects.get(name="team2"))
        grad3 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad3", email="grad3@barclays.com"), assigned_team=Team.objects.get(name="team3"))
        grad4 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad4", email="grad4@barclays.com"), assigned_team=Team.objects.get(name="team1"))
        grad5 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad5", email="grad5@barclays.com"), assigned_team=Team.objects.get(name="team3"))
        grad6 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad6", email="grad6@barclays.com"), assigned_team=Team.objects.get(name="team1"))
        grad7 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad7", email="grad7@barclays.com"), assigned_team=Team.objects.get(name="team3"))
        grad8 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad8", email="grad8@barclays.com"), assigned_team=Team.objects.get(name="team2"))
        grad9 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad9", email="grad9@barclays.com"), assigned_team=Team.objects.get(name="team2"))
        grad10 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad10", email="grad10@barclays.com"))


        graduates = {
            'grad1':{'team1':5,'team2':1,'team3':3},
            'grad2':{'team1':1,'team2':2,'team3':5},
            'grad3':{'team1':2,'team2':3,'team3':3},
            'grad4':{'team1':4,'team2':5,'team3':2},
            'grad5':{'team1':3,'team2':3,'team3':1},
            'grad6':{'team1':2,'team2':3,'team3':1},
            'grad7':{'team1':1,'team2':2,'team3':3},
            'grad8':{'team1':2,'team2':2,'team3':4},
		    'grad9':{'team1':3,'team2':1,'team3':5},
		    'grad10':{'team1':5,'team2':1,'team3':2}
        }


        for grad,pref_list in graduates.items():
            for team,weight in pref_list.items():
                Preference.objects.create(grad=Graduate.objects.get(user=CustomUser.objects.get(first_name=grad)), 
                                        team = Team.objects.get(name=team),
                                        weight = weight)

          

    def test_get_allocation(self):
        client = Client()
        user = CustomUser.objects.create_user(email="admin@barclays.com", password="1234", username="admin")
        logged_in = client.login(email='admin@barclays.com', password='1234', username='admin')
        # uncomment below to test with view call, however unable to test without reshuffling the graduates randomly, therefore tests will not pass
        # client.get(reverse('allocationapp:get_allocation'))
        # print(response)

        # calling allocation with testing argument = True, so that no random reshuffling occurs and allocation can be tested with hardcoded results below
        allocation_result = allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()), testing=True)
        print(allocation_result)

        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad5")).assigned_team, Team.objects.get(name="team1"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad7")).assigned_team, Team.objects.get(name="team1"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad3")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad4")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad6")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad1")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad2")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad8")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad9")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad10")).assigned_team, Team.objects.get(name="team3"))
