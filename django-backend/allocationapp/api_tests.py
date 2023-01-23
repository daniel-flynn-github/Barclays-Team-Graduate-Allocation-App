from django.test import TestCase
from allocationapp.models import Graduate, Team, Preference
from django.test import Client

class TestGetMatches(TestCase):
    def setUp(self):
        grad1 = Graduate.objects.get_or_create()
        grad2 = Graduate()
        grad3 = Graduate()
        grad4 = Graduate()
        grad5 = Graduate()
        grad6 = Graduate()
        grad7 = Graduate()
        grad8 = Graduate()

        team1 = Team(capacity=3)
        team2 = Team(capacity=4)
        team3 = Team(capacity=5)

        graduates = {
            'grad1':{'team1':100,'team2':1,'team3':3},
            'grad2':{'team1':1,'team2':100,'team3':5},
            'grad3':{'team1':2,'team2':3,'team3':100},
            'grad4':{'team1':100,'team2':5,'team3':2,},
            'grad5':{'team1':3,'team2':100,'team3':3},
            'grad6':{'team1':2,'team2':3,'team3':1},
            'grad7':{'team1':1,'team2':2,'team3':100},
            'grad8':{'team1':2,'team2':100,'team3':4}
        }

        for grad,pref_list in graduates.items():
            for team,weight in pref_list.items():
                Preference.objects.create(gradId=grad.user.id, teamId=team.id, weight=weight)

          

    def test_get_allocation(self):
        c = Client()
        logged_in = c.login(username='', password='')
        self.assertTrue(logged_in)
        response = c.get('allocationapp:get_allocation')
        print(response)
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
        
    
