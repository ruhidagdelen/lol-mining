################################
# lol-mining project
# date: 12.11.2018
# author: R U hi?
# version: 2.1
################################
import requests
import sys
import pandas as pd
from requests import exceptions

riotAPI = "RGAPI-b31e88c9-f07e-4e7d-bf2f-bfd5607cdceb"
seasonID = "11"
endIndex = "5"
winnerEndIndex = "5"
ROLEFLAG = 0


def requestSummonerData(summonerName):
    # Here is how I make my URL.  There are many ways to create these.
    URL = "https://tr1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + riotAPI
    # requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    if response.status_code == 404:
        print("We couldn't find your Account try again")
        print("due to 404")
        main()
    else:
        return response.json()


def requestMatchList(accountID, seasonID, endIndex):
    URL = "https://tr1.api.riotgames.com/lol/match/v3/matchlists/by-account/" + accountID + "?endIndex=" + endIndex + "&queue=420&queue=440&season=" + seasonID + "&api_key=" + riotAPI
    response = requests.get(URL)
    return response.json()


def requestMatchDetail(matchID):
    URL = "https://tr1.api.riotgames.com/lol/match/v3/matches/" + matchID + "?api_key=" + riotAPI
    response = requests.get(URL)
    return response.json()


def staticsCalculator(account, role):
    gameDuration = 0.0
    totalDamageDealtToChampions = 0.0
    longestTimeSpentLiving = 0.0
    totalMinionsKilled = 0.0
    visionScore = 0.0
    kills = 0.0
    deaths = 0.0
    assists = 0.0
    largestKillingSpree = 0.0
    largestMultiKill = 0.0
    killingSprees = 0.0
    longestTimeSpentLiving = 0.0
    doubleKills = 0.0
    tripleKills = 0.0
    quadraKills = 0.0
    pentaKills = 0.0
    unrealKills = 0.0
    totalDamageDealt = 0.0
    magicDamageDealt = 0.0
    physicalDamageDealt = 0.0
    trueDamageDealt = 0.0
    largestCriticalStrike = 0.0
    totalDamageDealtToChampions = 0.0
    magicDamageDealtToChampions = 0.0
    physicalDamageDealtToChampions = 0.0
    trueDamageDealtToChampions = 0.0
    totalHeal = 0.0
    totalUnitsHealed = 0.0
    damageSelfMitigated = 0.0
    damageDealtToObjectives = 0.0
    damageDealtToTurrets = 0.0
    timeCCingOthers = 0.0
    totalDamageTaken = 0.0
    physicalDamageTaken = 0.0
    magicalDamageTaken = 0.0
    trueDamageTaken = 0.0
    goldEarned = 0.0
    goldSpent = 0.0
    turretKills = 0.0
    inhibitorKills = 0.0
    neutralMinionsKilled = 0.0
    totalTimeCrowdControlDealt = 0.0
    champLevel = 0.0
    visionWardsBoughtInGame = 0.0
    sightWardsBoughtInGame = 0.0
    wardsPlaced = 0.0
    wardsKilled = 0.0

    matchlistResponse = requestMatchList(str(account), seasonID, endIndex)
    matchIDList = getMatchIDs(matchlistResponse)
    print("%d's matches \n" % account)
    print(matchIDList)
    for j in matchIDList:
        matchDetailResponse = requestMatchDetail(j)
        gameDuration = float(matchDetailResponse['gameDuration'])
        for i in range(len(matchIDList)):
            if matchDetailResponse['participantIdentities'][i]['player']['currentAccountId'] == account:
                summonerName = matchDetailResponse['participantIdentities'][i]['player']['summonerName']

                totalDamageDealtToChampions += float(
                    matchDetailResponse['participants'][i]['stats']['totalDamageDealtToChampions']) / gameDuration
                longestTimeSpentLiving += float(
                    matchDetailResponse['participants'][i]['stats']['longestTimeSpentLiving']) / gameDuration
                totalMinionsKilled += float(
                    matchDetailResponse['participants'][i]['stats']['totalMinionsKilled']) / gameDuration
                visionScore += float(matchDetailResponse['participants'][i]['stats']['visionScore']) / gameDuration
                kills += float(matchDetailResponse['participants'][i]['stats']['kills']) / gameDuration
                deaths += float(matchDetailResponse['participants'][i]['stats']['deaths']) / gameDuration
                assists += float(matchDetailResponse['participants'][i]['stats']['assists']) / gameDuration
                largestKillingSpree += float(
                    matchDetailResponse['participants'][i]['stats']['largestKillingSpree']) / gameDuration
                largestMultiKill += float(
                    matchDetailResponse['participants'][i]['stats']['largestMultiKill']) / gameDuration
                killingSprees += float(matchDetailResponse['participants'][i]['stats']['killingSprees']) / gameDuration
                longestTimeSpentLiving += float(
                    matchDetailResponse['participants'][i]['stats']['longestTimeSpentLiving']) / gameDuration
                doubleKills += float(matchDetailResponse['participants'][i]['stats']['doubleKills']) / gameDuration
                tripleKills += float(matchDetailResponse['participants'][i]['stats']['tripleKills']) / gameDuration
                quadraKills += float(matchDetailResponse['participants'][i]['stats']['quadraKills']) / gameDuration
                pentaKills += float(matchDetailResponse['participants'][i]['stats']['pentaKills']) / gameDuration
                unrealKills += float(matchDetailResponse['participants'][i]['stats']['unrealKills']) / gameDuration
                totalDamageDealt += float(
                    matchDetailResponse['participants'][i]['stats']['totalDamageDealt']) / gameDuration
                magicDamageDealt += float(
                    matchDetailResponse['participants'][i]['stats']['magicDamageDealt']) / gameDuration
                physicalDamageDealt += float(
                    matchDetailResponse['participants'][i]['stats']['physicalDamageDealt']) / gameDuration
                trueDamageDealt += float(
                    matchDetailResponse['participants'][i]['stats']['trueDamageDealt']) / gameDuration
                largestCriticalStrike += float(
                    matchDetailResponse['participants'][i]['stats']['largestCriticalStrike']) / gameDuration
                totalDamageDealtToChampions += float(
                    matchDetailResponse['participants'][i]['stats']['totalDamageDealtToChampions']) / gameDuration
                magicDamageDealtToChampions += float(
                    matchDetailResponse['participants'][i]['stats']['magicDamageDealtToChampions']) / gameDuration
                physicalDamageDealtToChampions += float(
                    matchDetailResponse['participants'][i]['stats']['physicalDamageDealtToChampions']) / gameDuration
                trueDamageDealtToChampions += float(
                    matchDetailResponse['participants'][i]['stats']['trueDamageDealtToChampions']) / gameDuration
                totalHeal += float(
                    matchDetailResponse['participants'][i]['stats']['totalHeal']) / gameDuration

                totalUnitsHealed += float(
                    matchDetailResponse['participants'][i]['stats']['totalUnitsHealed']) / gameDuration
                damageSelfMitigated += float(
                    matchDetailResponse['participants'][i]['stats']['damageSelfMitigated']) / gameDuration
                damageDealtToObjectives += float(
                    matchDetailResponse['participants'][i]['stats']['damageDealtToObjectives']) / gameDuration
                damageDealtToTurrets += float(
                    matchDetailResponse['participants'][i]['stats']['damageDealtToTurrets']) / gameDuration
                timeCCingOthers += float(
                    matchDetailResponse['participants'][i]['stats']['timeCCingOthers']) / gameDuration
                totalDamageTaken += float(
                    matchDetailResponse['participants'][i]['stats']['totalDamageTaken']) / gameDuration
                magicalDamageTaken += float(
                    matchDetailResponse['participants'][i]['stats']['magicalDamageTaken']) / gameDuration
                physicalDamageTaken += float(
                    matchDetailResponse['participants'][i]['stats']['physicalDamageTaken']) / gameDuration
                trueDamageTaken += float(
                    matchDetailResponse['participants'][i]['stats']['trueDamageTaken']) / gameDuration
                goldEarned += float(
                    matchDetailResponse['participants'][i]['stats']['goldEarned']) / gameDuration
                goldSpent += float(
                    matchDetailResponse['participants'][i]['stats']['goldSpent']) / gameDuration
                turretKills += float(
                    matchDetailResponse['participants'][i]['stats']['turretKills']) / gameDuration
                inhibitorKills += float(
                    matchDetailResponse['participants'][i]['stats']['inhibitorKills']) / gameDuration
                neutralMinionsKilled += float(
                    matchDetailResponse['participants'][i]['stats']['neutralMinionsKilled']) / gameDuration
                totalTimeCrowdControlDealt += float(
                    matchDetailResponse['participants'][i]['stats']['totalTimeCrowdControlDealt']) / gameDuration
                champLevel += float(
                    matchDetailResponse['participants'][i]['stats']['champLevel']) / gameDuration
                visionWardsBoughtInGame += float(
                    matchDetailResponse['participants'][i]['stats']['visionWardsBoughtInGame']) / gameDuration
                sightWardsBoughtInGame += float(
                    matchDetailResponse['participants'][i]['stats']['sightWardsBoughtInGame']) / gameDuration
                wardsPlaced += float(
                    matchDetailResponse['participants'][i]['stats']['wardsPlaced']) / gameDuration
                wardsKilled += float(
                    matchDetailResponse['participants'][i]['stats']['wardsKilled']) / gameDuration
                break

    print(summonerName + " s stats for last games as " + role)

    print("Aggression Point")
    avgDamageDealtToChampions = totalDamageDealtToChampions / len(matchIDList)
    print(avgDamageDealtToChampions)

    print("\nSurvival Point")
    avglongestTimeSpentLiving = longestTimeSpentLiving / len(matchIDList)
    print(avglongestTimeSpentLiving)

    print("\nFarming Point")
    avgtotalMinionsKilled = totalMinionsKilled / len(matchIDList)
    print(avgtotalMinionsKilled)

    print("\nVision Point")
    avgvisionScore = visionScore / len(matchIDList)
    print(avgvisionScore)

    return {"0 Summoner Name": summonerName,
            # "1- Summoner Role": role,
            "1- DamageDealtToChampions": avgDamageDealtToChampions,
            "2- longestTimeSpentLiving": avglongestTimeSpentLiving,
            "3- totalMinionsKilled": avgtotalMinionsKilled,
            "4- visionScore": avgvisionScore,
            "kills": kills / len(matchIDList),
            "deaths": deaths / len(matchIDList),
            "assists": assists / len(matchIDList),
            "largestKillingSpree": largestKillingSpree / len(matchIDList),
            "largestMultiKill": largestMultiKill / len(matchIDList),
            "killingSprees": killingSprees / len(matchIDList),
            "longestTimeSpentLiving": longestTimeSpentLiving / len(matchIDList),
            "doubleKills  ": doubleKills   / len(matchIDList),
            "tripleKills ": tripleKills  / len(matchIDList),
            "quadraKills ": quadraKills  / len(matchIDList),
            "pentaKills ": pentaKills  / len(matchIDList),
            "unrealKills ": unrealKills  / len(matchIDList),
            "totalDamageDealt ": totalDamageDealt  / len(matchIDList),
            "magicDamageDealt ": magicDamageDealt  / len(matchIDList),
            "physicalDamageDealt ": physicalDamageDealt  / len(matchIDList),
            "trueDamageDealt ": trueDamageDealt  / len(matchIDList),
            "largestCriticalStrike ": largestCriticalStrike  / len(matchIDList),
            "totalDamageDealtToChampions ": totalDamageDealtToChampions  / len(matchIDList),
            "magicDamageDealtToChampions ": magicDamageDealtToChampions  / len(matchIDList),
            "physicalDamageDealtToChampions ": physicalDamageDealtToChampions  / len(matchIDList),
            "trueDamageDealtToChampions ": trueDamageDealtToChampions  / len(matchIDList),
            "totalHeal  ": totalHeal  / len(matchIDList),
            "totalUnitsHealed  ": totalUnitsHealed  / len(matchIDList),
            "damageSelfMitigated  ": damageSelfMitigated  / len(matchIDList),
            "damageDealtToObjectives  ": damageDealtToObjectives  / len(matchIDList),
            "damageDealtToTurrets  ": damageDealtToTurrets  / len(matchIDList),
            "timeCCingOthers  ": timeCCingOthers  / len(matchIDList),
            "totalDamageTaken  ": totalDamageTaken  / len(matchIDList),
            "physicalDamageTaken  ": physicalDamageTaken  / len(matchIDList),
            # "magicDamageTaken  ": magicDamageTaken  / len(matchIDList),
            "trueDamageTaken  ": trueDamageTaken  / len(matchIDList),
            "goldEarned  ": goldEarned  / len(matchIDList),
            "goldSpent  ": goldSpent  / len(matchIDList),
            "turretKills  ": turretKills  / len(matchIDList),
            "inhibitorKills  ": inhibitorKills  / len(matchIDList),
            "neutralMinionsKilled  ": neutralMinionsKilled  / len(matchIDList),
            "totalTimeCrowdControlDealt  ": totalTimeCrowdControlDealt  / len(matchIDList),
            "champLevel   ": champLevel  / len(matchIDList),
            "visionWardsBoughtInGame   ": visionWardsBoughtInGame  / len(matchIDList),
            "sightWardsBoughtInGame   ": sightWardsBoughtInGame  / len(matchIDList),
            "wardsPlaced   ": wardsPlaced  / len(matchIDList),
            "wardsKilled   ": wardsKilled  / len(matchIDList),
            }


def getMatchIDs(matchlistResponse):
    matchIDList = []
    for i in range(0, (int)(endIndex)):
        matchIDList.append((str)(matchlistResponse['matches'][i]['gameId']))
    return matchIDList


def findWinners(matchIDList, account, role, roleSec):
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
                    if matchDetailResponse['participantIdentities'][i]['player'][
                        'currentAccountId'] not in winnerIDList:
                        winnerIDList.append(
                            matchDetailResponse['participantIdentities'][i]['player']['currentAccountId'])
                        break
                    break
    return winnerIDList


def main():
    summonerName = (str)(input('Enter Name: >'))
    role = (str)(input('Enter Role: >'))
    roleSec = (str)(input('Enter Secondary Role: >'))

    # =============================================================================

    accountResponse = requestSummonerData(summonerName)
    print("YOUR ACCOUNT ID: >")
    print(accountResponse['accountId'])
    accountID = (str)(accountResponse['accountId'])

    # =============================================================================

    matchlistResponse = requestMatchList(accountID, seasonID, endIndex)

    matchIDList = getMatchIDs(matchlistResponse)
    print("\nYOUR MATCH HISTORY: >")
    print(matchIDList)

    # =============================================================================

    winners = findWinners(matchIDList, accountID, role, roleSec)
    print("\nPLAYERS WHO WON AT " + role + " AND " + roleSec + " ROLE")
    print(winners)
    df = pd.DataFrame()
    for key in range(len(winners)):
        if key < ROLEFLAG:
            df = df.append(staticsCalculator(winners[key], role), ignore_index=True)
        else:
            df = df.append(staticsCalculator(winners[key], roleSec), ignore_index=True)
        if key >= int(winnerEndIndex) - 1:
            break
    print(df)
    writer = pd.ExcelWriter('lolregression.xlsx')
    df.to_excel(writer)
    writer.save()


if __name__ == "__main__":
    main()
