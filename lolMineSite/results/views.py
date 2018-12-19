from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from .forms import PlayerForm
from .api.api import *
import json
from django.http import JsonResponse
from pyahp import parse
import math
import operator

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
            prios = pd.DataFrame({'prioritie':priorities})
            print(prios)
            players = players.join(prios)
            print(players)
            players = players.sort_values(by=['prioritie'],ascending=False)
            print(players)
            
            return render(request, 'results/results.html',{'players':players['player'],
                'aggressions':players['aggression'],
                'farms':players['farm'],
                'survives':players['survive'],
                'visions':players['vision'],
                'priorities':players['prioritie']})
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
    'kills': 0.2414,
    'totalDamageDealtToChampions': -0.00001
    }
    constant = -0.02271289
    raw = main(query.username, query.main_role, query.secondary_role)
    # raw = pd.read_excel('results/api/lolLive.xlsx')
    # raw = {'live':raw}
    if raw == 404:
        return False,False

    df = pd.DataFrame(raw['live'])
    Wps = []
    for key,row in df.iterrows():
        x = constant + row['regAssist']*regConst['assists']+row['regVisionScore']*regConst['visionScore']+row['regTimeCCingOthers']*regConst['timeCCingOthers']+row['regDeaths']*regConst['deaths']+row['regKills']*regConst['kills']+row['regTotalDamageDealtToChampions']*regConst['totalDamageDealtToChampions']
        wp = math.exp(x)/(1+math.exp(x))
        print(wp)
        Wps.append(wp)
        
    WP = pd.DataFrame({'wp':Wps})
    df = df.join(WP)
    print(df)
    df = df.sort_values(by=['wp'])
    print('afterSort')
    print(df)
    return df,True

def welcome(request):
    return render(request, 'results/welcome.html', {})

def prepAhp(query):
    raw,chck = regression(query)
    if not chck:
        return 404,404
    raw = raw.sort_index()
    players = raw['Summoner Name']
    aggressions = raw['Aggression Point']
    farms = raw['Farming Point']
    survives = raw['Survival Point']
    visions = raw['Vision Point']
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
    df = pd.DataFrame({'player':players,'aggression':aggressions,'farm':farms,'survive':survives,'vision':visions})
    df = df.sort_index()
    return data,df.head(4)