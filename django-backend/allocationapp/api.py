from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
import allocationapp.allocation
from allocationapp.models import Graduate, Team, Preference
#from django.urls import reverse

@login_required
def get_allocation(request):
    # Get the user asking for allocation
    # get all grads and check if user is in there
    user = request.user
    if user.role == 2: # to be tested
        return JsonResponse({'status':'false','message':'Not allowed to enter page'}, status=500)
    # Call the matching algorithm to get the data here
    allocation_list = []
    allocation_results = allocationapp.allocation.run_allocation()
    for team,team_members in allocation_results.items():
        allocation_list.append({
            "team": team,
            "graduates": team_members,
        })

    # Set safe to False because we want to return a list of results and not a single object
    return JsonResponse(allocation_list, safe=False)