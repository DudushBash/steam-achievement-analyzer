import requests
import os
import pandas as pd

url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
url2 = "https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/"
steam_key = os.getenv("STEAM_API_KEY")

def find_achiv(game_id):
    param = {
        "gameid": game_id,
        "format": "json"
    }
    response2 = requests.get(url2, params=param)
    data2 = response2.json()
    if "achievementpercentages" not in data2:
        print("У игры нет достижений или API вернул ошибку")
        return
    achiv = data2["achievementpercentages"]["achievements"]
    sorted_ach = sorted(achiv,key=lambda x: float(x["percent"]))
    print("Top 10 rarest achievements:")
    for ah in sorted_ach[:10]:
        print(f'{ah["name"]} = {ah["percent"]}%')

def find_games(game_name):
    row = df[df["name"].str.lower().str.contains(game_name, na=False)]
    if row.empty:
        print("Nah")
        return None
    game_id = row.iloc[0]["appid"]
    return game_id


if os.path.exists("games.csv"):
    df = pd.read_csv("games.csv")
else:
    stemke = {
        "key": steam_key,
        "max_results": 1000
    }
    response = requests.get(url, params=stemke)
    data = response.json()
    games = data["response"]["apps"]
    df = pd.DataFrame(games)
    df.to_csv("games.csv", index=False)

game_name = input("Введите игру: ").lower()
game_id = find_games(game_name)
if game_id:
    find_achiv(game_id)