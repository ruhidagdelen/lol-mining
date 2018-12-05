from django.shortcuts import render
from django.http import HttpResponse
from .forms import PlayerForm
from .api.api import *

def index(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.save()
            result = main(player.username,player.main_role,player.secondary_role)
            return render(request, 'results/results.html',{'result':result['live'],
            	'all_data':result['collected'],
            	'range':range(len(result['live'])),
            	'range2':range(len(result['collected']))})
    else:
        form = PlayerForm()
    return render(request, 'results/index.html', {'form':form})

def about(request):
    return render(request, 'results/about.html', {})

def how_to(request):
    return render(request, 'results/how_to.html', {})

