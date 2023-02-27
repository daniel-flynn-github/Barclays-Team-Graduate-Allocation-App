from django.test import TestCase, Client
from .models import *
from .views import *
from django.urls import reverse
from . import allocation

class TestModelStringRepresentations(TestCase):
    def setUp(self):
        Team.objects.create(name = "team", capacity=3, lower_bound=2)
        Graduate.objects.create(user=CustomUser.objects.create(first_name="grad", email="grad@barclays.com"), assigned_team=Team.objects.get(name="team"))
        Department.objects.create(name="mock_department")
        Manager.objects.create(user=CustomUser.objects.create(first_name="manager", email="manager@barclays.com"))
        Skill.objects.create(name="problem solving")
        Technology.objects.create(name="Python")
        Admin.objects.create(user=CustomUser.objects.create(first_name="admin", email="admin@barclays.com"))
        Preference.objects.create(graduate=Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")), 
                                    team = Team.objects.get(name="team"),
                                    weight = 3)
    
    def testStringRepresentations(self):
        team = Team.objects.get(name="team")
        self.assertEqual(str(team), f"'{team.name}' -> teamID: {team.id}")
        grad = Graduate.objects.get(user=CustomUser.objects.get(first_name="grad"))
        self.assertEqual(str(grad), f"GRADUATE | {grad.user}")
        department = Department.objects.get(name="mock_department")
        self.assertEqual(str(department), f"{department.name} Department")
        manager = Manager.objects.get(user=CustomUser.objects.get(first_name="manager"))
        self.assertEqual(str(manager), f"MANAGER | {manager.user}")
        skill = Skill.objects.get(name="problem solving")
        self.assertEqual(str(skill), f"{skill.name}")
        technology = Technology.objects.get(name="Python")
        self.assertEqual(str(technology), f"{technology.name}")
        admin = Admin.objects.get(user=CustomUser.objects.get(first_name="admin"))
        self.assertEqual(str(admin), f"ADMIN | {admin.user}")
        preference = Preference.objects.get(graduate=Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")), 
                                        team = Team.objects.get(name="team"))
        self.assertEqual(str(preference), f"{preference.graduate.user.email} -> {preference.weight} votes for {preference.team.name}")

class TestGraduateModel(TestCase):
    def setUp(self):
        team = Team.objects.create(name = "team", capacity=3, lower_bound=2)
        grad = Graduate.objects.create(user=CustomUser.objects.create(first_name="grad", email="grad@barclays.com"), assigned_team=Team.objects.get(name="team"))

    def testGraduateModel(self):
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")).assigned_team, Team.objects.get(name="team"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")).user.email, "grad@barclays.com")

class TestTeamModel(TestCase):
    def setUp(self):
        default_team = Team.objects.create(name="default_team", capacity=3)
        mock_department = Department.objects.create(name="mock_department")
        mock_manager = Manager.objects.create(user=CustomUser.objects.create(first_name="manager", email="manager@barclays.com"))
        skill1 = Skill.objects.create(name="problem solving")
        skill2 = Skill.objects.create(name="data science")
        technology1 = Technology.objects.create(name="Python")
        technology2 = Technology.objects.create(name="R")
        complete_team = Team.objects.create(
            name="complete_team", 
            description="This is a test team", 
            capacity=5, 
            lower_bound=3,
            department=mock_department,
            manager=mock_manager)
        complete_team.skills.add(skill1)
        complete_team.skills.add(skill2)
        complete_team.technologies.add(technology1)
        complete_team.technologies.add(technology2)

    def testDefaultFieldsOfIncompleteTeamInstance(self):
        self.assertEqual(Team.objects.get(name="default_team").capacity, 3)
        self.assertEqual(Team.objects.get(name="default_team").lower_bound, 1)
    
    def testFieldsOfCompleteTeamInstance(self):
        self.assertEqual(Team.objects.get(name="complete_team").description, "This is a test team")
        self.assertEqual(Team.objects.get(name="complete_team").capacity, 5)
        self.assertEqual(Team.objects.get(name="complete_team").lower_bound, 3)
        self.assertEqual(Team.objects.get(name="complete_team").department, Department.objects.get(name="mock_department"))
        self.assertEqual(Team.objects.get(name="complete_team").manager, Manager.objects.get(user=CustomUser.objects.get(first_name="manager")))
        self.assertEqual(Team.objects.get(name="complete_team").skills.all()[0], Skill.objects.get(name="problem solving"))      
        self.assertEqual(Team.objects.get(name="complete_team").skills.all()[1], Skill.objects.get(name="data science"))      
        self.assertEqual(Team.objects.get(name="complete_team").technologies.all()[0], Technology.objects.get(name="Python"))      
        self.assertEqual(Team.objects.get(name="complete_team").technologies.all()[1], Technology.objects.get(name="R"))      
    
    def testDeleteFieldBehaviour(self):
        Manager.objects.get(user=CustomUser.objects.get(first_name="manager")).delete()
        self.assertIsNone(Team.objects.get(name="complete_team").manager)
        Department.objects.get(name="mock_department").delete()
        self.assertFalse(Team.objects.filter(name="complete_team").exists())

class TestClientLogin(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(email="admin@barclays.com", password="1234", username="admin")
    def testLogin(self):
        client = Client()
        logged_in = client.login(email='admin@barclays.com', password='1234', username='admin')
        self.assertTrue(logged_in)

class TestIndexView(TestCase):
    def setUp(self):
        Graduate.objects.create(user=CustomUser.objects.create_user(first_name="grad", email="grad@barclays.com", username="grad", password="1234"))
        Manager.objects.create(user=CustomUser.objects.create_user(first_name="manager", email="manager@barclays.com", username="manager", password="1234"))
        Admin.objects.create(user=CustomUser.objects.create_user(first_name="admin", email="admin@barclays.com", username="admin", password="1234"))

    def testAdminIndex(self):
        self.client.login(email='admin@barclays.com', password='1234', username='admin')
        response = self.client.get(reverse("allocationapp:index"))
        self.assertRedirects(response, reverse('allocationapp:upload'), status_code=302, target_status_code=200)
    
    def testManagerIndex(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        response = self.client.get(reverse("allocationapp:index"))
        self.assertRedirects(response, reverse('allocationapp:manager_view_teams'), status_code=302, target_status_code=200)
    
    def testGraduateIndex(self):
        self.client.login(email='grad@barclays.com', password='1234', username='grad')
        response = self.client.get(reverse("allocationapp:index"))
        self.assertRedirects(response, reverse('allocationapp:cast_votes'), status_code=302, target_status_code=200)

class TestAllocation(TestCase):
    def setUp(self):
        # test database setup for alg test
        team1 = Team.objects.create(name = "team1", capacity=3, lower_bound=2)
        team2 = Team.objects.create(name = "team2", capacity=4, lower_bound=3)
        team3 = Team.objects.create(name = "team3", capacity=5, lower_bound=4)

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
                Preference.objects.create(graduate=Graduate.objects.get(user=CustomUser.objects.get(first_name=grad)), 
                                        team = Team.objects.get(name=team),
                                        weight = weight)

    def test_get_allocation(self):
        # calling allocation with testing argument = True, so that no random reshuffling occurs and allocation can be tested with hardcoded results below
        allocation_result = allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()), testing=True)
        #print(allocation_result)

        # unit tests to check that correct team has been allocated to each grad
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
