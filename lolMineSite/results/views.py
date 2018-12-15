from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import PlayerForm
from .api.api import *
import json
from django.http import JsonResponse
from pyahp import parse

def index(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.save()

            resAhp,players = prepAhp(query)
            
            # result = main(player.username,player.main_role,player.secondary_role)
            print(resAhp)
            ahp_model = parse(resAhp)
            priorities = ahp_model.get_priorities()
            # last = result['live']
            # last = map(list, last.values)
            # all_data = result['collected']
            # all_data = map(list, all_data.values)
            # # all_data = all_data.values.to_list()
            # return render(request, 'results/results.html',{
            # 	'result':last,
            # 	'all_data':all_data,
            # 	})
            return render(request, 'results/results.html',{'players':players,'priorities':priorities})
    else:
        form = PlayerForm()
    return render(request, 'results/index.html', {'form':form})

def about(request):
    return render(request, 'results/about.html', {})

def how_to(request):
    return render(request, 'results/how_it_works.html', {})

def prepAhp(query):
    raw = main(query.username, query.main_role, query.secondary_role)
    players = raw['live']['Summoner Name']
    aggressions = raw['live']['Aggression Point']
    farms = raw['live']['Farming Point']
    survives = raw['live']['Survival Point']
    visions = raw['live']['Vision Point']
    aggMatrix = [
        [1, aggressions[0]/aggressions[1], aggressions[0]/aggressions[2], aggressions[0]/aggressions[3]],
        [aggressions[1]/aggressions[0], 1, aggressions[1]/aggressions[2], aggressions[1]/aggressions[3]],
        [aggressions[2]/aggressions[0], aggressions[2]/aggressions[1], 1, aggressions[2]/aggressions[3]],
        [aggressions[3]/aggressions[0], aggressions[3]/aggressions[1], aggressions[3]/aggressions[2], 1]
    ]
    farmMatrix = [
        [1, farms[0]/farms[1], farms[0]/farms[2], farms[0]/farms[3]],
        [farms[1]/farms[0], 1, farms[1]/farms[2], farms[1]/farms[3]],
        [farms[2]/farms[0], farms[2]/farms[1], 1, farms[2]/farms[3]],
        [farms[3]/farms[0], farms[3]/farms[1], farms[3]/farms[2], 1]
    ]
    surviveMatrix = [
        [1, survives[0]/survives[1], survives[0]/survives[2], survives[0]/survives[3]],
        [survives[1]/survives[0], 1, survives[1]/survives[2], survives[1]/survives[3]],
        [survives[2]/survives[0], survives[2]/survives[1], 1, survives[2]/survives[3]],
        [survives[3]/survives[0], survives[3]/survives[1], survives[3]/survives[2], 1]
    ]
    visionMatrix = [
        [1, visions[0]/visions[1], visions[0]/visions[2], visions[0]/visions[3]],
        [visions[1]/visions[0], 1, visions[1]/visions[2], visions[1]/visions[3]],
        [visions[2]/visions[0], visions[2]/visions[1], 1, visions[2]/visions[3]],
        [visions[3]/visions[0], visions[3]/visions[1], visions[3]/visions[2], 1]
    ]
    print(aggMatrix)
    print(farmMatrix)
    print(surviveMatrix)
    print(visionMatrix)
    data = {"name": "Sample Model",
        "method": "approximate",
        "criteria": ["agg", "farm", "surv", "visio"],
        "subCriteria": {},
        "alternatives": [players[0],players[1],players[2],players[3]],
        "preferenceMatrices": {
            "criteria": [
                [1, query.aggOverFar, query.aggOverSur, query.aggOverVis],
                [1/query.aggOverFar, 1, query.farOverSur, query.farOverVis],
                [1/query.aggOverSur, 1/query.farOverSur, 1, query.surOverVis],
                [1/query.aggOverVis, 1/query.farOverVis, 1/query.surOverVis, 1]
            ],
            "alternatives:agg": aggMatrix,
            "alternatives:farm": farmMatrix,
            "alternatives:surv": surviveMatrix,
            "alternatives:visio": visionMatrix
        }
    }
    return data,players[:4]