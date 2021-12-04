'''
NHL Shot Charts
IDK the actual goal here ust gonna make them
'''

import matplotlib.pyplot as plt
import requests
from matplotlib import image
from hockey_rink import NHLRink
from PIL import Image
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import mplcursors

#All NYI games
nyi_schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?season=20202021&teamId=2&gameType=R")

url = requests.get("https://statsapi.web.nhl.com/api/v1/game/2021020355/feed/live")
content = url.json()

event = content["liveData"]
game_data = content["gameData"]
date = game_data["datetime"]
datetime = date["dateTime"]
datetime = datetime[0:10]
teams = game_data["teams"]
away = teams["away"]
home = teams["home"]
away_team = away["abbreviation"]
home_team = home["abbreviation"]
print(teams)
plays = event["plays"]
all_plays = plays["allPlays"]

fig=plt.figure(figsize=(10,10))
plt.xlim([0,100])
plt.ylim([-42.5, 42.5])


home_shot_attempts = 0
home_sog=0
home_goals=0
away_shot_attempts = 0
away_sog=0
away_goals=0
for i in all_plays:
    result = i["result"]
    event = result["event"]
    if event=="Goal" or event == "Shot" or event=="Missed Shot":
        team_info = i["team"]
        team = team_info["triCode"]
        if team == home_team:
            home_shot_attempts += 1
            print(team)
            print(event)
            coords = (i["coordinates"])
            print(coords)
            x = int(coords["x"])
            y = int(coords["y"])
            if x < 0:
                x = abs(x)
                y = y*-1
            else:
                x=x
                y=y
            print(i)
            if event=="Goal":
                home_goals+=1
                empty_net = result["emptyNet"]
                if empty_net != False:
                    continue
                else:
                    plt.plot(x, y, 'd', color="#4bad53",markersize=20)
            elif event=="Shot":
                home_sog+=1
                plt.plot(x, y, 'o', color="#f0a911",markersize=15)
            else:
                plt.plot(x, y, 'x', color="#000000",markersize=15)
        else:
            away_shot_attempts += 1
            print(team)
            print(event)
            coords = (i["coordinates"])
            print(coords)
            x = int(coords["x"])
            y = int(coords["y"])
            if x > 0:
                x = -x
                y =-y
            else:
                x=x
                y=y
            print(i)
            if event=="Goal":
                away_goals+=1
                empty_net = result["emptyNet"]
                if empty_net != False:
                    continue
                else:
                    plt.plot(x, y, 'd', color="#4bad53",markersize=20)
            elif event=="Shot":
                away_sog+=1
                plt.plot(x, y, 'o', color="#f0a911",markersize=15)
            else:
                plt.plot(x, y, 'x', color="#000000",markersize=15)
    else:
        continue


rink = NHLRink()
ax = rink.draw()
plt.title(away_team + " vs. " + home_team + "\n " + datetime + "\n" + away_team +": "+ str(away_shot_attempts) + " Total Shot Attempts " + "                                                                                                                                                                        "
          +  home_team + ": " + str(home_shot_attempts) + " Total Shot Attempts")
plt.show()
