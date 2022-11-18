from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse


def index(request):
    # This might return the login/landing page? Probably will be
    # Right now it just redirects to the cast_votes page
    return redirect(reverse('allocationapp:cast_votes'))

def cast_votes(request):
    # View function for the GRADUATE CAST VOTES page.
    context_dict = {}
    return render(request, 'allocationapp/cast_votes.html', context=context_dict)
