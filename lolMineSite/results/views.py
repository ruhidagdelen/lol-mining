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
            if resAhp == 404:
                e = 'Player Not Found'
                return render(request, 'results/not_found.html',{'notfound':e})
            
            # result = main(player.username,player.main_role,player.secondary_role)
            print(resAhp)
            ahp_model = parse(resAhp)
            try:
                priorities = ahp_model.get_priorities()
            except AssertionError as e:
                return render(request, 'results/not_found.html',{'consError':e})
            
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

def not_found(request):
    return render(request, 'results/not_found.html', {})

def criteria(request):
    return render(request, 'results/criteria.html', {})

def regression(query):
    regConst = {
    'assists': 0.2254,
    'visionScore': -0.0044,
    'timeCCingOthers': -0.0144,
    'deaths': -0.4347,
    'kills': -0.2414,
    'totalDamageDealtToChampions': -0.00001
    }
    raw = main(query.username, query.main_role, query.secondary_role)
    if raw == 404:
        return 404
    # regAssist = raw['live']['regAssist']
    # regVisionScore = raw['live']['regVisionScore']
    # regTimeCCingOthers = raw['live']['regTimeCCingOthers']
    # regDeaths = raw['live']['regDeaths']
    # regKills = raw['live']['regKills']
    # regTotalDamageDealtToChampions = raw['live']['regTotalDamageDealtToChampions']

    for row in raw['live']:
        pass

def welcome(request):
    return render(request, 'results/welcome.html', {})

def prepAhp(query):
    raw = main(query.username, query.main_role, query.secondary_role)
    if raw == 404:
        return 404,404
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