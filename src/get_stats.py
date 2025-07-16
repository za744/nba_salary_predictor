from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import time

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
        data.append(df)
        time.sleep(1)
    
    return pd.concat(data, ignore_index=False)

if __name__ == "__main__":
    player_list = ["LeBron James", "Kyrie Irving", "Cade Cunningham", "Anthony Davis"]
    df=get_top_players(player_list)
    df.to_csv("data/raw/player_stats.csv", index=False)

