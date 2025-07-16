from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import time
import random

def get_player_name(player_name):
    player_dict = players.find_players_by_full_name(player_name)[0]
    stats = playercareerstats.PlayerCareerStats(player_id=player_dict["id"])
    df=stats.get_data_frames()[0]
    df["PLAYER_NAME"] = player_name
    return df

def get_top_players(player_list):
    data = []
    for name in player_list:
        df=get_player_name(name)
        if df is not None and not df.empty:
            data.append(df)
        time.sleep(1)
    
    return pd.concat(data, ignore_index=False)

active_players = players.get_active_players()
player_names=[p["full_name"] for p in active_players]

minutes_data = []
for name in player_names:
    try:
        player_id = players.find_players_by_full_name(name)[0]
        stats=playercareerstats.PlayerCareerStats(player_id=player_id)
        df=stats.get_data_frames()[0]
        latest_minutes = (df.sort_values("SEASON_ID", ascending=False)).iloc[0]
        minutes=latest_minutes["MIN"]
        minutes_data.append((minutes, name))

    except:
        continue

minutes_df=pd.DataFrame(minutes_data, columns=["MIN", "PLAYER_NAME"])
top_100_minutes= minutes_df.sort_values("MIN", ascending=False).head(100)["PLAYER_NAME"].tolist()

other_players=list(set(player_names) - set(top_100_minutes))
random_200 = random.sample(other_players, 200)

final_players = top_100_minutes + random_200

df_players=get_top_players(final_players)
df_players.to_csv("data/raw/player_stats.csv", index=False)


#if __name__ == "__main__":
    #player_list = ["LeBron James", "Kyrie Irving", "Cade Cunningham", "Anthony Davis"]
    #df=get_top_players(player_list)
    #df.to_csv("data/raw/player_stats.csv", index=False)

