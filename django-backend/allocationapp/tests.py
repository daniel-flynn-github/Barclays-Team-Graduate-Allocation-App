from django.test import TestCase, Client
from .models import *
from .views import *
from .utilities import *
from django.urls import reverse
from . import allocation
from .allocation import run_allocation
import json

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
        self.assertRedirects(response, reverse('allocationapp:portal'), status_code=302, target_status_code=200)
    
    def testManagerIndex(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        response = self.client.get(reverse("allocationapp:index"))
        self.assertRedirects(response, reverse('allocationapp:manager_view_teams'), status_code=302, target_status_code=200)
    
    def testGraduateIndex(self):
        self.client.login(email='grad@barclays.com', password='1234', username='grad')
        response = self.client.get(reverse("allocationapp:index"))
        self.assertRedirects(response, reverse('allocationapp:cast_votes'), status_code=302, target_status_code=200)

class TestGraduateViews(TestCase):
    def setUp(self):
        Graduate.objects.create(user=CustomUser.objects.create_user(first_name="grad", email="grad@barclays.com", username="grad", password="1234"))
        Team.objects.create(name = "team1", capacity=3, lower_bound=2)
        Team.objects.create(name = "team2", capacity=4, lower_bound=3)

    def testCastVotes(self):
        self.client.login(email='grad@barclays.com', password='1234', username='grad')
        url = reverse("allocationapp:cast_votes")
        data = {'votes': json.dumps({'%s' % Team.objects.get(name="team1").id: 5, '%s' % Team.objects.get(name="team2").id: 3})}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('allocationapp:vote_submitted'), status_code=302, target_status_code=200)
        self.assertEqual(Preference.objects.filter(graduate=Graduate.objects.get(user=CustomUser.objects.get(first_name="grad"))).count(), 2)
        self.assertEqual(Preference.objects.get(graduate=Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")), team=Team.objects.get(name="team1")).weight, 5)
        self.assertEqual(Preference.objects.get(graduate=Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")), team=Team.objects.get(name="team2")).weight, 3)
    
    def testViewTeams(self):
        self.client.login(email='grad@barclays.com', password='1234', username='grad')
        url = reverse('allocationapp:cast_votes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allocationapp/cast_votes.html')
        teams_displayed = response.context['teams']
        self.assertEqual(len(teams_displayed), 2)
        self.assertEqual(teams_displayed[0].name, 'team1')
        self.assertEqual(teams_displayed[1].name, 'team2')
    
    def testVoteSubmitted(self):
        self.client.login(email='grad@barclays.com', password='1234', username='grad')
        url = reverse('allocationapp:vote_submitted')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allocationapp/vote_submitted.html')
        self.assertEqual(response.context["current_graduate"], Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")))
    
    def testResultPageBeforeAllocation(self):
        AllocationState.objects.create(has_allocated=False)
        self.client.login(email='grad@barclays.com', password='1234', username='grad')
        url = reverse('allocationapp:result_page')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('allocationapp:cast_votes'), status_code=302, target_status_code=200)
    
    def testResultPageAfterAlocation(self):
        AllocationState.objects.create(has_allocated=True)
        self.client.login(email='grad@barclays.com', password='1234', username='grad')
        url = reverse('allocationapp:result_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allocationapp/result_page.html')

class TestManagerViews(TestCase):
    def setUp(self):
        Manager.objects.create(user=CustomUser.objects.create_user(first_name="manager", email="manager@barclays.com", username="manager", password="1234"))
        Manager.objects.create(user=CustomUser.objects.create_user(first_name="manager2", email="manager2@barclays.com", username="manager2", password="1234"))
        Department.objects.create(name="dep1")
        Department.objects.create(name="dep2")
        Skill.objects.create(name="problem solving")
        Skill.objects.create(name="data science")
        Technology.objects.create(name="Python")
        Technology.objects.create(name="R")
        Team.objects.create(name = "team1", capacity=3, lower_bound=2, manager=Manager.objects.get(user=CustomUser.objects.get(first_name="manager")), department=Department.objects.get(name="dep1"))
        Team.objects.get(name="team1").skills.add(Skill.objects.get(name="data science"))
        Team.objects.get(name="team1").technologies.add(Technology.objects.get(name="R"))
        Team.objects.create(name = "team2", capacity=4, lower_bound=3, manager=Manager.objects.get(user=CustomUser.objects.get(first_name="manager")), department=Department.objects.get(name="dep2"))
        Team.objects.create(name = "team3", capacity=3, lower_bound=2)
        Graduate.objects.create(user=CustomUser.objects.create_user(first_name="grad", email="grad@barclays.com", username="grad", password="1234"), assigned_team=Team.objects.get(name="team1"))
        Graduate.objects.create(user=CustomUser.objects.create_user(first_name="grad2", email="grad2@barclays.com", username="grad2", password="1234"))

    def testManagerViewTeams(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        url = reverse('allocationapp:manager_view_teams')
        response = self.client.get(url)
        teams = response.context["teams"]
        self.assertEqual(len(teams), 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["team_members"][Team.objects.get(name="team1").id]), [Graduate.objects.get(user=CustomUser.objects.get(first_name="grad"))])
        self.assertEqual(list(response.context["graduates_with_no_team"]), [Graduate.objects.get(user=CustomUser.objects.get(first_name="grad2"))])
        self.assertTemplateUsed(response, 'allocationapp/manager_teams.html')
    
    def testManagerChangingTeamForGraduate(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        url = reverse('allocationapp:manager_view_teams')
        data = {'selected_grad': CustomUser.objects.get(first_name="grad2").id, 'team_id': Team.objects.get(name="team2").id}
        response = self.client.post(url, data)
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad2")).assigned_team, Team.objects.get(name="team2"))
    
    def testManagerDeletingGraduateFromTeam(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        url = reverse('allocationapp:delete_team_member', args=[CustomUser.objects.get(first_name="grad").id])
        response = self.client.post(url)
        self.assertIsNone(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad")).assigned_team)
    
    def testManagerDeletingTeamMemberFromTeamTheyDoNotOwn(self):
        # Manager tries to access a delete_team URL for a team they do not own.
        self.client.login(email='manager2@barclays.com', password='1234', username='manager2')
        url = reverse('allocationapp:delete_team_member', args=[CustomUser.objects.get(first_name="grad").id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('allocationapp:manager_view_teams'), status_code=302, target_status_code=200)

    def testManagerEditingTeamTheyDoNotOwn(self):
        # Manager tries to access an edit_team URL for a team they don't own.
        self.client.login(email='manager2@barclays.com', password='1234', username='manager2')
        url = reverse('allocationapp:manager_edit_team', args=[Team.objects.get(name="team1").id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('allocationapp:manager_view_teams'), status_code=302, target_status_code=200)

    def testManagerEditingTeamFunctionality(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        url = reverse('allocationapp:manager_edit_team', args=[Team.objects.get(name="team1").id])
        data = {
            'department_id': Department.objects.get(name="dep2").id,
            'chosen_technologies': [Technology.objects.get(name="Python").id],
            'chosen_skills': [Skill.objects.get(name="problem solving").id],
            'chosen_capacity': 5,
            'chosen_description': 'Newly changed team'
        }
        response = self.client.post(url, data)
        self.assertEqual(Team.objects.get(name="team1").department, Department.objects.get(name="dep2"))
        self.assertEqual(Team.objects.get(name="team1").technologies.count(), 1)
        self.assertEqual(list(Team.objects.get(name="team1").technologies.all()), [Technology.objects.get(name="Python")])
        self.assertEqual(Team.objects.get(name="team1").skills.count(), 1)
        self.assertEqual(list(Team.objects.get(name="team1").skills.all()), [Skill.objects.get(name="problem solving")])
        self.assertRedirects(response, reverse('allocationapp:manager_view_teams'), status_code=302, target_status_code=200)
        self.assertEqual(Team.objects.get(name="team1").capacity, 5)
        self.assertEqual(Team.objects.get(name="team1").description, "Newly changed team")
    
    def testManagerEditingTeamDisplay(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        url = reverse('allocationapp:manager_edit_team', args=[Team.objects.get(name="team1").id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'allocationapp/edit_team.html')
    
    def testManagerAddingNewSkill(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        url = reverse('allocationapp:manager_add_skill', args=[Team.objects.get(name="team1").id, "Code Reviewing"])
        response = self.client.get(url)
        # check if it exists in the first place
        self.assertTrue(Skill.objects.filter(name='Code Reviewing').exists())
        # check if it is assigned to team 1
        self.assertTrue(Team.objects.get(name="team1").skills.filter(name='Code Reviewing').exists())
        self.assertRedirects(response, reverse('allocationapp:manager_edit_team', args=[Team.objects.get(name="team1").id]), status_code=302, target_status_code=200)
    
    def testManagerAddingSkillThatAlreadyExists(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        skill = Skill.objects.create(name="Pre-assigned Skill")
        Team.objects.get(name="team1").skills.add(skill)
        self.assertEqual(Team.objects.get(name="team1").skills.filter(name='Pre-assigned Skill').count(), 1)
        url = reverse('allocationapp:manager_add_skill', args=[Team.objects.get(name="team1").id, "Pre-assigned Skill"])
        response = self.client.get(url)
        self.assertEqual(Team.objects.get(name="team1").skills.filter(name='Pre-assigned Skill').count(), 1)
        self.assertRedirects(response, reverse('allocationapp:manager_edit_team', args=[Team.objects.get(name="team1").id]), status_code=302, target_status_code=200)

    def testManagerAddingNewSkillToTeamTheyDontOwn(self):
        self.client.login(email='manager2@barclays.com', password='1234', username='manager2')
        url = reverse('allocationapp:manager_add_skill', args=[Team.objects.get(name="team1").id, "Code Reviewing"])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('allocationapp:manager_view_teams'), status_code=302, target_status_code=200)

    def testManagerAddingNewTechnology(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        url = reverse('allocationapp:manager_add_tech', args=[Team.objects.get(name="team1").id, "C#"])
        response = self.client.get(url)
        # check if it exists in the first place
        self.assertTrue(Technology.objects.filter(name='C#').exists())
        # check if it is assigned to team 1
        self.assertTrue(Team.objects.get(name="team1").technologies.filter(name='C#').exists())
        self.assertRedirects(response, reverse('allocationapp:manager_edit_team', args=[Team.objects.get(name="team1").id]), status_code=302, target_status_code=200)

    def testManagerAddingTechnologyThatAlreadyExists(self):
        self.client.login(email='manager@barclays.com', password='1234', username='manager')
        technology = Technology.objects.create(name="Pre-assigned Technology")
        Team.objects.get(name="team1").technologies.add(technology)
        self.assertEqual(Team.objects.get(name="team1").technologies.filter(name='Pre-assigned Technology').count(), 1)
        url = reverse('allocationapp:manager_add_tech', args=[Team.objects.get(name="team1").id, "Pre-assigned Technology"])
        response = self.client.get(url)
        self.assertEqual(Team.objects.get(name="team1").technologies.filter(name='Pre-assigned Technology').count(), 1)
        self.assertRedirects(response, reverse('allocationapp:manager_edit_team', args=[Team.objects.get(name="team1").id]), status_code=302, target_status_code=200)

    def testManagerAddingNewTechnplogyToTeamTheyDontOwn(self):
        self.client.login(email='manager2@barclays.com', password='1234', username='manager2')
        url = reverse('allocationapp:manager_add_tech', args=[Team.objects.get(name="team1").id, "Code Reviewing"])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('allocationapp:manager_view_teams'), status_code=302, target_status_code=200)

class TestUtilitiesFunctions(TestCase):
    def setUp(self):
        Graduate.objects.create(user=CustomUser.objects.create_user(first_name="grad", email="grad@barclays.com", username="grad", password="1234"))
        Manager.objects.create(user=CustomUser.objects.create_user(first_name="manager", email="manager@barclays.com", username="manager", password="1234"))
        Admin.objects.create(user=CustomUser.objects.create_user(first_name="admin", email="admin@barclays.com", username="admin", password="1234"))

    def testIsGrad(self):
        self.assertTrue(is_grad(CustomUser.objects.get(first_name="grad")))
        self.assertFalse(is_manager(CustomUser.objects.get(first_name="grad")))
        self.assertFalse(is_admin(CustomUser.objects.get(first_name="grad")))
    
    def testIsManager(self):
        self.assertFalse(is_grad(CustomUser.objects.get(first_name="manager")))
        self.assertTrue(is_manager(CustomUser.objects.get(first_name="manager")))
        self.assertFalse(is_admin(CustomUser.objects.get(first_name="manager")))
    
    def testIsAdmin(self):
        self.assertFalse(is_grad(CustomUser.objects.get(first_name="admin")))
        self.assertFalse(is_manager(CustomUser.objects.get(first_name="admin")))
        self.assertTrue(is_admin(CustomUser.objects.get(first_name="admin")))
    
    def testResetUsers(self):
        reset_users()
        self.assertFalse(CustomUser.objects.filter(first_name="admin").exists())
        self.assertFalse(CustomUser.objects.filter(first_name="grad").exists())
        self.assertFalse(CustomUser.objects.filter(first_name="manager").exists())

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
       
        for grad in Graduate.objects.all():
            grad.assigned_team = None


    def test_graduates_equal_capacity(self):
        team3 = Team.objects.get(name='team3')
        team3.capacity = 3
        team3.lower_bound = 1
        team3.save()

        allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()), testing=True)
        
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad5")).assigned_team, Team.objects.get(name="team1"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad8")).assigned_team, Team.objects.get(name="team1"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad10")).assigned_team, Team.objects.get(name="team1"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad3")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad4")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad6")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad7")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad1")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad2")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad9")).assigned_team, Team.objects.get(name="team3"))
        for grad in Graduate.objects.all():
            grad.assigned_team = None

    def test_graduates_equal_lower_bound(self):
        team3 = Team.objects.get(name='team3')
        team3.capacity = 5
        team3.lower_bound = 5
        team3.save()
        allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()), testing=True)
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad5")).assigned_team, Team.objects.get(name="team1"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad10")).assigned_team, Team.objects.get(name="team1"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad3")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad4")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad7")).assigned_team, Team.objects.get(name="team2"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad1")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad2")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad6")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad8")).assigned_team, Team.objects.get(name="team3"))
        self.assertEqual(Graduate.objects.get(user=CustomUser.objects.get(first_name="grad9")).assigned_team, Team.objects.get(name="team3"))
        for grad in Graduate.objects.all():
            grad.assigned_team = None

    def test_uncomplete_preference(self):
        team3 = Team.objects.get(name='team3')
        team3.capacity = 5
        team3.lower_bound = 2
        team3.save()
        grad1_preferences=Preference.objects.filter(graduate = Graduate.objects.get(user = CustomUser.objects.get(first_name="grad1")))
        grad1_preferences.all().delete()
        allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()), testing=True)
        for pref in grad1_preferences:
            self.assertTrue(pref.weight == 100 or pref.weight == 0)
    
    def test_same_preferences_max(self):
        preferences = Preference.objects.all()
        for pref in preferences:
            pref.weight == 5
            pref.save()
        allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()), testing=True)
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

    def test_same_preferences_min(self):
        preferences = Preference.objects.all()
        for pref in preferences:
            pref.weight == 0
            pref.save()
        allocation.run_allocation(list(Graduate.objects.all()), list(Team.objects.all()), testing=True)
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


