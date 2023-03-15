import networkx as nx
import random
import math
import itertools

from allocationapp.models import Preference, CustomUser


def increase_preference_weight_for_previous_team_to_discourage(graduates):
    for graduate in graduates:
        if graduate.assigned_team != None:
            preference, created = Preference.objects.get_or_create(
                graduate=graduate, 
                team=graduate.assigned_team,
                defaults={'weight': 100}  # default to weight 100 if no preference has been cast.
            )
            
            # Graduate already cast their preference? Add 100 to the weight.
            if not created:
                preference.weight += 100
                preference.save()


# function using networkx library to run a min_cost_max_flow
# with_lower_bound attribute is False by default, if true the algorithm is run capping the team capacities at the lower bound


def run_min_cost_max_flow(graduates, teams, with_lower_bound=False):
    G = nx.DiGraph()

    # each graduate is a node in the network
    for graduate in graduates:
        G.add_node(graduate, demand=-1)

    # each team is a node in the network
    if (with_lower_bound):
        for team in teams:
            G.add_node(team, demand=team.lower_bound)
    else:
        # teams will be a dictionary only if run_min_cost_max_flow is run on the second run of an allocation with a lower bound with more vacancies than graduates
        if type(teams) == dict:
            for team, capacity in teams.items():
                G.add_node(team, demand=capacity)
        else:
            for team in teams:
                G.add_node(team, demand=team.capacity)

    for graduate in graduates:
        for team in teams:
            if not (Preference.objects.filter(graduate=graduate, team=team)).exists():
                Preference.objects.create(graduate=graduate, team=team, weight=0)
            # 6 - to revert the scale from 1 to 5
            if (Preference.objects.get(graduate=graduate, team=team).weight >= 100):
                G.add_edge(graduate, team, weight=Preference.objects.get(
                    graduate=graduate, team=team).weight)
            else:
                # 6 - to revert the scale from 1 to 5
                G.add_edge(graduate, team, weight=6 -
                           (Preference.objects.get(graduate=graduate, team=team).weight))

    flowDict = nx.min_cost_flow(G)

    return flowDict


def run_allocation(all_graduates, all_teams, testing=False):
    increase_preference_weight_for_previous_team_to_discourage(all_graduates)
    total_vacancies = 0
    vacancies_on_lower_bound = 0
    for team in all_teams:
        total_vacancies += team.capacity
        print(team.name + ' capacity: ' + str(team.capacity))
        vacancies_on_lower_bound += team.lower_bound

    if len(all_graduates) > total_vacancies:
        print("Error: not enough spaces for graduates")
        exit()

    if len(all_graduates) < vacancies_on_lower_bound:
        print("Error: not enough graduates to satisfy lower bound")
        exit()

    # alg run only once when total vacancies equal the amount of graduates
    if len(all_graduates) == total_vacancies:
        first_run_allocation = run_min_cost_max_flow(all_graduates, all_teams)
        allocation_result = {team: [] for team in all_teams}
        # assign teams to each graduate
        for graduate in first_run_allocation:
            for team in first_run_allocation[graduate]:
                if(first_run_allocation[graduate][team] == 1):
                    graduate.assigned_team = team
                    graduate.save()
                    allocation_result[team].append(graduate)
    # alg will need to be run twice when there are more vacancies than graduates
    else:
        # randomly shuffle graduates to randomise who gets picked for first or second run
        # (since first-run people are more likely to get their preferred team)
        if (not testing):
            random.shuffle(all_graduates)
        randomly_sampled_grads_for_first_run = all_graduates[:vacancies_on_lower_bound]
        randomly_sampled_grads_for_second_run = all_graduates[vacancies_on_lower_bound:]
        # alg first run
        first_run_allocation = run_min_cost_max_flow(
            randomly_sampled_grads_for_first_run, all_teams, with_lower_bound=True)
        remaining_spaces = total_vacancies - vacancies_on_lower_bound
        # modify team capacity based on graduates left and remaining spaces in the team (becuase they need to be equal)
        remaining_teams = {}
        integers = []
        fractions = {}
        for team in all_teams:
            frac, whole = math.modf((team.capacity-team.lower_bound) *
                                    (len(randomly_sampled_grads_for_second_run)/remaining_spaces))
            remaining_teams[team] = int(whole)
            integers.append(whole)
            fractions[team] = frac
        needed = len(randomly_sampled_grads_for_second_run) - sum(integers)
        fractions = {k: v for k, v in sorted(
            fractions.items(), key=lambda item: item[1])[::-1]}
        for k, v in dict(itertools.islice(fractions.items(), int(needed))).items():
            remaining_teams[k] += 1
        # alg second run
        second_run_allocation = run_min_cost_max_flow(
            randomly_sampled_grads_for_second_run, remaining_teams)

        allocation_result = {team: [] for team in all_teams}
        # assign teams to each graduate
        for graduate in first_run_allocation:
            for team in first_run_allocation[graduate]:
                if(first_run_allocation[graduate][team] == 1):
                    graduate.assigned_team = team
                    graduate.save()
                    allocation_result[team].append(graduate)
        for graduate in second_run_allocation:
            for team in second_run_allocation[graduate]:
                if(second_run_allocation[graduate][team] == 1):
                    graduate.assigned_team = team
                    graduate.save()
                    allocation_result[team].append(graduate)
        

    #TESTING REMOVE
    for team,grads in allocation_result.items():
        print(team.name + ': '+ ', '.join([grad.user.first_name for grad in grads]) + '\n')
