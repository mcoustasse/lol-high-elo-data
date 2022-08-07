from riotwatcher import LolWatcher
import pandas as pd


def get_match_list(summoner, num_matches, player_routing, lol_watcher):
    """
    Description:
        Get the match list for a specific player
    Input:
        summoner: LolWatcher summoner object
        num_matches: int
        player_routing: str
        lol_watcher: LolWatcher
    Output:
        match_list: list of match ids
    """
    match_history = lol_watcher.match.matchlist_by_puuid(
        region=player_routing,
        puuid=summoner["puuid"],
        queue=420,
        start=0,
        count=num_matches,
    )

    return match_history


def get_game_info(matchID, player_routing, lol_watcher):
    """
    Description:
        Get the game info for a specific match
    Input:
        matchID: str
        player_routing: str
        lol_watcher: LolWatcher
    Output:
        game_info: pd.DataFrame object
    """

    # API request to get match info
    match_info = lol_watcher.match.by_id(region=player_routing, match_id=matchID)[
        "info"
    ]
    # Get the game id for a specific match
    game_id = match_info["gameId"]

    # Create empty lists to store data
    puuid = list()
    lane = list()
    champ_name = list()
    kda = list()
    win = list()

    # Iterate through each participant in the game (always 10)
    for i in range(10):

        aux_puuid = match_info["participants"][i]["puuid"]
        aux_lane = match_info["participants"][i]["individualPosition"]
        aux_champ_name = match_info["participants"][i]["championName"]
        aux_kda = match_info["participants"][i]["challenges"]["kda"]
        aux_win = match_info["participants"][i]["win"]
        puuid.append(aux_puuid)
        lane.append(aux_lane)
        champ_name.append(aux_champ_name)
        kda.append(aux_kda)
        win.append(aux_win)

    df = pd.DataFrame(
        {
            "game_id": game_id,
            "puuid": puuid,
            "lane": lane,
            "champ_name": champ_name,
            "kda": kda,
            "win": win,
        },
        columns=["game_id", "puuid", "lane", "champ_name", "kda", "win"],
    )

    return df


def get_challenger_players(player_region, queue_type, lol_watcher):
    """
    Description:
        Get the challenger players for a specific region and queue type
    Input:
        player_region: str
        queue_type: str
        lol_watcher: LolWatcher
    Output:
        challenger_players: list of summoner names
    """
    challenger_ladder = lol_watcher.league.challenger_by_queue(
        region=player_region, queue=queue_type
    )
    challenger_players = pd.DataFrame.from_dict(challenger_ladder["entries"])
    challenger_players_list = challenger_players["summonerId"].tolist()

    return challenger_players_list
