import networkx as nx
import random
import math
import itertools

from allocationapp.models import Graduate, Team, Preference

allGraduates = list(Graduate.objects.all())
allTeams = list(Team.objects.all())
total_vacancies = 0
for team in allTeams:
    total_vacancies += team.capacity
lower_bound = 3
vacancies_on_lower_bound = len(allTeams) * lower_bound

def run_min_cost_max_flow(graduates, teams, with_lower_bound=False):
    G = nx.DiGraph()

    for grad in graduates:
        G.add_node(grad, demand=-1)

    if (with_lower_bound):
        for team in teams:
            G.add_node(team, demand=lower_bound)
    else:
        for team in teams:
            G.add_node(team, demand=team.capacity)

    for grad in graduates:
        for team in teams:
            G.add_edge(grad, team, weight=Preference.objects.get(gradId=grad.id, teamId=team.id).weight) #to be changed

    flowDict = nx.min_cost_flow(G)

    return flowDict

def run_allocation():
    if len(allGraduates) > total_vacancies:
        print("Error: not enough spaces for graduates")
        exit()

    if len(allGraduates) < vacancies_on_lower_bound:
        print("Error: not enough grads to satisfy lower bound")
        exit()

    if len(allGraduates) == total_vacancies:
        allocation_result = run_min_cost_max_flow(allGraduates,allTeams)
    elif len(allGraduates) > vacancies_on_lower_bound:
        randomly_shuffled_grads = random.shuffle(allGraduates)
        randomly_sampled_grads_for_first_run = randomly_shuffled_grads[:lower_bound*len(allTeams)]
        randomly_sampled_grads_for_second_run = randomly_shuffled_grads[lower_bound*len(allTeams):]
        first_run_allocation = run_min_cost_max_flow(randomly_sampled_grads_for_first_run, allTeams, with_lower_bound=True)
        remaining_spaces = total_vacancies - vacancies_on_lower_bound
        remaining_teams = {}
        integers = []
        fractions = {}
        for team in allTeams:
            frac,whole = math.modf((team.capacity-lower_bound)*(len(randomly_sampled_grads_for_second_run)/remaining_spaces))
            remaining_teams[team] = int(whole)
            integers.append(whole)
            fractions[team] = frac
        needed = len(randomly_sampled_grads_for_second_run) - sum(integers)
        fractions = {k: v for k, v in sorted(fractions.items(), key=lambda item: item[1])[::-1]}
        for k,v in dict(itertools.islice(fractions.items(), int(needed))).items():
            remaining_teams[k] += 1
        second_run_allocation = run_min_cost_max_flow(randomly_sampled_grads_for_second_run,remaining_teams)

        allocation_result = {team:[] for team in allTeams}

        for grad in first_run_allocation:
            for team in first_run_allocation[grad]:
                if(first_run_allocation[grad][team] == 1):
                    allocation_result[team].append(grad)
            for team in second_run_allocation[grad]:
                if(second_run_allocation[grad][team] == 1):
                    allocation_result[team].append(grad)
    
    return allocation_result
