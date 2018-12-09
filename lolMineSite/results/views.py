from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import PlayerForm
from .api.api import *

def index(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.save()
            result = main(player.username,player.main_role,player.secondary_role)
            resAhp = prepAhp(player.aggOverFar,
            	player.aggOverSur,
            	player.aggOverVis,
            	player.farOverSur,
            	player.farOverVis,
            	player.surOverVis)
            last = result['live']
            last = map(list, last.values)
            all_data = result['collected']
            all_data = map(list, all_data.values)
            # all_data = all_data.values.to_list()
            return render(request, 'results/results.html',{
            	'result':last,
            	'all_data':all_data,
            	})
    else:
        form = PlayerForm()
    return render(request, 'results/index.html', {'form':form})

def about(request):
    return render(request, 'results/about.html', {})

def how_to(request):
    return render(request, 'results/how_to.html', {})

def prepAhp(aggOverFar,aggOverSur,aggOverVis,farOverSur,farOverVis,surOverVis):
	return 0