#################################
# lol-mining project            #
# date: 12.11.2018              #
# author: ruhiddin              #
# version: 2.1                  #
#################################
import requests
import sys
import os
import time
import pandas as pd
from requests import exceptions

riotAPI = "RGAPI-56e0891d-4bf0-498e-ace5-6b653a9b0d6f"
seasonID = "11"
endIndex = "10" #should be endIndex => winnerEndIndex 
winnerEndIndex = "10"
ROLEFLAG = 0
REQUEST_FLAG = 0

def requestCountCheck():
    global REQUEST_FLAG
    if REQUEST_FLAG >= 100:
        print('Please wait! Program will be avaliable..')
        time.sleep(35)
        print('in 60 sec')
        time.sleep(20)
        print('in 30 sec')
        time.sleep(15)
        print('in 10 sec')
        time.sleep(10)
        REQUEST_FLAG = 0
        return True
    else:
        REQUEST_FLAG += 1
        print(REQUEST_FLAG)
        return True 

def requestSummonerData(summonerName):
    # Here is how I make my URL.  There are many ways to create these.
    URL = "https://tr1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + riotAPI
    # requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
    requestCountCheck()
    response = requests.get(URL)
    if response.status_code == 404:
        print("We couldn't find your Account try again")
        print("due to 404")
        main()
    else:
        return response.json()


def requestMatchList(accountID, seasonID, endIndex):
    URL = "https://tr1.api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID + "?endIndex=" + endIndex + "&queue=420&queue=440&season=" + seasonID + "&api_key=" + riotAPI
    requestCountCheck()
    response = requests.get(URL)
    return response.json()


def requestMatchDetail(matchID):
    URL = "https://tr1.api.riotgames.com/lol/match/v3/matches/" + matchID + "?api_key=" + riotAPI
    requestCountCheck()
    response = requests.get(URL)
    return response.json()
    

def staticsCalculator(account,role):
    gameDuration = 0.0
    totalDamageDealtToChampions = 0.0
    longestTimeSpentLiving = 0.0
    totalMinionsKilled = 0.0
    visionScore = 0.0
    damage = 0 
    living = 0
    lastHit = 0
    vision = 0
    summonerName = ""

    matchlistResponse = requestMatchList(str(account),seasonID,endIndex)
    matchIDList = getMatchIDs(matchlistResponse)
    print("%d's matches \n" %account)
    print(matchIDList)
    for j in matchIDList:
        matchDetailResponse = requestMatchDetail(j)
        print(matchDetailResponse['gameDuration'])
        gameDuration = (float)(matchDetailResponse['gameDuration'])
        for i in range(len(matchIDList)):
            if matchDetailResponse['participantIdentities'][i]['player']['currentAccountId'] == account:
                summonerName = matchDetailResponse['participantIdentities'][i]['player']['summonerName']

                damage += matchDetailResponse['participants'][i]['stats']['totalDamageDealtToChampions']
                living += matchDetailResponse['participants'][i]['stats']['longestTimeSpentLiving']
                lastHit += matchDetailResponse['participants'][i]['stats']['totalMinionsKilled']
                vision += matchDetailResponse['participants'][i]['stats']['visionScore']

                totalDamageDealtToChampions += float(
                    matchDetailResponse['participants'][i]['stats']['totalDamageDealtToChampions']) / gameDuration
                longestTimeSpentLiving += float(
                    matchDetailResponse['participants'][i]['stats']['longestTimeSpentLiving']) / gameDuration
                totalMinionsKilled += float(
                    matchDetailResponse['participants'][i]['stats']['totalMinionsKilled']) / gameDuration
                visionScore += float(matchDetailResponse['participants'][i]['stats']['visionScore']) / gameDuration
                break
    print(summonerName + " s stats for last games as "+ role)
    print("Aggression Point")
    agression = totalDamageDealtToChampions / len(matchIDList)
    print(agression)
    print("\nSurvival Point")
    survival = longestTimeSpentLiving / len(matchIDList)
    print(survival)
    print("\nFarming Point")
    farming = totalMinionsKilled / len(matchIDList)
    print(farming)
    print("\nVision Point")
    visPoint = visionScore / len(matchIDList)
    print(visPoint)
    print("\n")
    _damage = damage/len(matchIDList)
    print("Total Damage Dealt: "+ str(_damage))
    _living = living/len(matchIDList)
    print("\n Longest time alive: "+ str(_living))
    _lastHit = lastHit/len(matchIDList)
    print("\n Total creeps killed: "+ str(_lastHit))
    _vision = vision/len(matchIDList)
    print("\n Vision: "+ str(_vision))
    return {"Summoner Name": summonerName,
            "Summoner Role": role,
            "Aggression Point": agression,
            "Survival Point": survival,
            "Farming Point": farming,
            "Vision Point": visPoint,
            "Average Damage": _damage,
            "Longest Alive": _living,
            "Last Hit":_lastHit,
            "Vision": _vision}


def getMatchIDs(matchlistResponse):
    matchIDList = []
    for i in range(0, (int)(endIndex)):
        matchIDList.append((str)(matchlistResponse['matches'][i]['gameId']))
    return matchIDList


def findWinners(matchIDList,account,role,roleSec):
    global ROLEFLAG
    winnerIDList = []
    tempMatchDetail = []
    for j in matchIDList:
        matchDetailResponse = requestMatchDetail(j)
        tempMatchDetail.append(matchDetailResponse)
        for i in range(9):
            if (str)(matchDetailResponse['participants'][i]['stats']['win']) == "True" and (str)(
                    matchDetailResponse['participants'][i]['timeline']['role']) == role:
                if (str)(matchDetailResponse['participantIdentities'][i]['player']['currentAccountId']) == account:
                    continue
                if matchDetailResponse['participantIdentities'][i]['player']['currentAccountId'] not in winnerIDList:
                    winnerIDList.append(matchDetailResponse['participantIdentities'][i]['player']['currentAccountId'])
                    break
    ROLEFLAG = len(winnerIDList)
    while len(winnerIDList) < int(winnerEndIndex):
        for j in tempMatchDetail:
            matchDetailResponse = j
            for i in range(9):
                if (str)(matchDetailResponse['participants'][i]['stats']['win']) == "True" and (str)(
                        matchDetailResponse['participants'][i]['timeline']['role']) == roleSec:
                    if (str)(matchDetailResponse['participantIdentities'][i]['player']['currentAccountId']) == account:
                        continue
                    if matchDetailResponse['participantIdentities'][i]['player']['currentAccountId'] not in winnerIDList:
                        winnerIDList.append(matchDetailResponse['participantIdentities'][i]['player']['currentAccountId'])
                        break
                    break
    return winnerIDList


def checkRoles(role,roleSec):
    avaliable = ['DUO', 'NONE', 'SOLO', 'DUO_CARRY', 'DUO_SUPPORT']
    if role and roleSec in avaliable:
        return True
    else:
        print('Check the roles! '+role+' or '+roleSec+' not avaliable')
        print('Avaliable Roles: >')
        print(avaliable)
        main()

def wannaContinue():
    status = (str)(input('Press enter to Contunie or type "exit" to exit!'))
    print('++'+status+'++')
    status = status.lower()
    if status == "exit":
        sys.exit()
    else:
        main()

def main():
    summonerName = (str)(input('Enter Name: >'))
    role = (str)(input('Enter Role: >'))
    roleSec = (str)(input('Enter Secondary Role: >'))
    role = role.upper()
    roleSec = roleSec.upper()
    print(role,roleSec)

    checkRoles(role,roleSec)
    # =============================================================================
    
    accountResponse = requestSummonerData(summonerName)
    print(accountResponse)
    print("YOUR ACCOUNT ID: >"+str(accountResponse['accountId']))
    # print(accountResponse['accountId'])
    accountID = (str)(accountResponse['accountId'])

    # =============================================================================
    
    matchlistResponse = requestMatchList(accountID, seasonID, endIndex)
    
    matchIDList = getMatchIDs(matchlistResponse)
    print("\nYOUR MATCH HISTORY: >")
    print(matchIDList)
    
    # =============================================================================
    
    winners = findWinners(matchIDList,accountID,role,roleSec)
    print("\nPLAYERS WHO WON AT " + role + " AND " + roleSec + " ROLE")
    print(winners)
    df = pd.DataFrame()
    for key in range(len(winners)):
        if key < ROLEFLAG:
            df = df.append(staticsCalculator(winners[key],role),ignore_index=True)
        else:
            df = df.append(staticsCalculator(winners[key],roleSec),ignore_index=True)
        if key >= int(winnerEndIndex)-1:
            break
    print(df)

    os.remove('lolLive.xlsx')
    writer = pd.ExcelWriter('lolLive.xlsx')
    df.to_excel(writer)
    writer.save()

    collected_data = pd.read_excel('lol.xlsx')
    collected_data = collected_data.append(df,ignore_index=True)
    collected_data = collected_data.drop_duplicates()
    print(collected_data)

    os.remove('lol.xlsx')
    collector = pd.ExcelWriter('lol.xlsx')
    collected_data.to_excel(collector)
    collector.save()

    wannaContinue()

if __name__ == "__main__":
    main()
