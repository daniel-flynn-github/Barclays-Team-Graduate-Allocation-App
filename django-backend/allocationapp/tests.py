from django.test import TestCase
from models import Graduate, Team, Preference, CustomUser
from django.test import Client

class TestGetAllocation(TestCase):
    def setUp(self):
        grad1 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad1"))
        grad3 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad2"))
        grad4 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad3"))
        grad5 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad4"))
        grad6 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad5"))
        grad7 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad6"))
        grad8 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad7"))
        grad2 = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad8"))

        team1 = Team(name = "team1", capacity=3)
        team2 = Team(name = "team2", capacity=4)
        team3 = Team(name = "team3", capacity=5)

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
