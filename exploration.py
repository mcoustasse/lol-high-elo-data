##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher
from dotenv import load_dotenv
import os
import pandas as pd
from sys import getsizeof


def total_games(player_info):
    total_games = player_info["wins"] + player_info["losses"]
    return total_games


# MAIN CODE

##--------- LOAD CONFIG DATA ---------##
api_key = "RGAPI-cec446f4-378e-4eaf-874b-d342d622c770"
lol_watcher = LolWatcher(api_key)

##--------- GET THE RAW DATA ---------##
player_region = "LA2".lower()  # [BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]
player_routing = "americas"
queue_type = "RANKED_SOLO_5x5"  # RANKED_SOLO_5x5, RANKED_FLEX_SR,
challenger_ladder = lol_watcher.league.challenger_by_queue(
    region=player_region, queue=queue_type
)

raw_data = pd.DataFrame.from_dict(
    challenger_ladder
)  # convert the challenger info to dataframe
print(raw_data.head())
print("Fields= ", list(raw_data))


##--------- EXTRACT RELEVANT DATA ---------##
# print('\nENTRIES= \n', challenger_ladder['entries'][0:3])
challenger_players = pd.DataFrame.from_dict(
    challenger_ladder["entries"]
)  # we only really care about the entries
print(challenger_players.head())
print("Fields= ", list(challenger_players))


##--------- CLEAN UP DATA ---------##
# print('\n', challenger_players[['summonerName','leaguePoints']].head()) #run this a couple times, note un-ordered

challenger_players = challenger_players.sort_values(
    by="leaguePoints", ascending=False
)  # organize into leaderboard
challenger_players.reset_index(drop=True, inplace=True)  # reset index to match order
print(
    "\n", challenger_players[["summonerName", "leaguePoints", "wins", "losses"]].head()
)


##--------- LOOKING AT A SPECIFIC PLAYER ---------##
# Instead of adding columns, we only want to work with a single element -> convert to dict
num1_player = challenger_players.loc[
    challenger_players["summonerName"] == "FIX 10"
].to_dict("records")[0]
n_player_name = challenger_players.iloc[50]["summonerName"]
n_player = challenger_players.loc[
    challenger_players["summonerName"] == n_player_name
].to_dict("records")[0]

##--------- LOAD THE PLAYER DATA AS CLASS ---------##
summoner = lol_watcher.summoner.by_name(player_region, n_player_name)
match_history = lol_watcher.match.matchlist_by_puuid(
    region=player_routing, puuid=summoner["puuid"], queue=420, start=0, count=1
)
matchID = match_history[0]

match_data_small = lol_watcher.match.by_id(region=player_routing, match_id=matchID)[
    "info"
]["participants"][0]["challenges"]["kda"]

print(match_data_small)
