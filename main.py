from extract import get_match_list
from extract import get_game_info
from extract import get_challenger_players
from riotwatcher import LolWatcher
import pandas as pd

##--------- LOAD CONFIG DATA ---------##
api_key = "RGAPI-0d9f3ede-7823-460f-8633-0c3a203859d5"
lol_watcher = LolWatcher(api_key)

##--------- PARAMETERS ---------##
player_region = "LA2".lower()  # [BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]
player_routing = "americas"
queue_type = "RANKED_SOLO_5x5"  # RANKED_SOLO_5x5, RANKED_FLEX_SR,
num_matches = 100

##--------- GET CHALLENGER PLAYERS ---------##
challenger_players = get_challenger_players(player_region, queue_type, lol_watcher)

for player in challenger_players:
    print(f"Getting data for player {player}")
    summoner = lol_watcher.summoner.by_id(player_region, player)
    last_100_matches = get_match_list(
        summoner, num_matches, player_routing, lol_watcher
    )
    for matchID in last_100_matches:
        if matchID == last_100_matches[0]:
            game_info = get_game_info(matchID, player_routing, lol_watcher)
        else:
            aux_game_info = get_game_info(matchID, player_routing, lol_watcher)
            game_info = pd.concat([game_info, aux_game_info])

print(game_info)

game_info.reset_index(drop=True).to_parquet(
    "game_info.parquet.gzip", compression="gzip"
)
