__author__ = 'wyunchi'

import urllib2, urllib, httplib
import json
import pymongo
import time

VALVE_ACCESS_TOKEN = '6FA3B90A9ECFC00FE4FEE4B558F80B5D'
DAC_LEAGUE_ID = 2339

conn = pymongo.Connection()
dota2_db = conn.dota2
current_matches_collection = dota2_db.current_matches

hero_collection = dota2_db.heros
item_collection = dota2_db.items
lobby_collection = dota2_db.lobbies
ability_collection = dota2_db.abilibties


def combine_parameter(parameters):
    result = ""
    for (key, value) in parameters.items():
        result = result + str(key) + '=' + str(value) + '&'
    result = result + 'key=' + VALVE_ACCESS_TOKEN
    return result


def get_parts_of_list(api_url, parameters):
    url = api_url + '?' + combine_parameter(parameters)
    print url
    try:
        url_read_handle = urllib2.urlopen(url, timeout=10)
        url_read_data = json.loads(''.join(url_read_handle.readlines()))
    except:
        return json.loads("{}")
    return url_read_data


def get_valve_web_result(api_url, parameters):
    result = get_parts_of_list(api_url, parameters)
    try:
        results_remaining = result['result']['results_remaining']
    except KeyError:
        return result
    while not results_remaining == 0:
        match_list = result['result']['matches']
        parameters['start_match_id'] = match_list[-1]['match_id'] - 1
        try:
            url_read_data = get_parts_of_list(api_url, parameters)
            results_remaining = url_read_data['result']['results_remaining']
            result['matches'].extend(url_read_data['result']['matches'])
        except KeyError:
            pass
    return result



'''
dota2 web api from http://dev.dota2.com/showthread.php?t=58317
(GetMatchHistory)              https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/
(GetMatchDetails)              https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v001/
(GetHeroes)                    https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/
(GetPlayerSummaries)           https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/
(EconomySchema)                https://api.steampowered.com/IEconItems_570/GetSchema/v0001/
(GetLeagueListing)             https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/
(GetLiveLeagueGames)           https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/
(GetMatchHistoryBySequenceNum) https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v0001/
(GetTeamInfoByTeamID)          https://api.steampowered.com/IDOTA2Match_570/GetTeamInfoByTeamID/v001/
'''


def get_match_history(hero_id=None,
                      game_mode=None,
                      skill=None,
                      min_players=None,
                      account_id=None,
                      league_id=None,
                      start_at_match_id=None,
                      matches_requested=None,
                      tournament_games_only=None):
    '''
    hero_id=<id>                   # Search for matches with a specific hero being played (hero ID, not name, see HEROES below)
    game_mode=<mode>               # Search for matches of a given mode (see below)
    skill=<skill>                  # 0 for any, 1 for normal, 2 for high, 3 for very high skill (default is 0)
    min_players=<count>            # the minimum number of players required in the match
    account_id=<id>                # Search for all matches for the given user (32-bit or 64-bit steam ID)
    league_id=<id>                 # matches for a particular league
    start_at_match_id=<id>         # Start the search at the indicated match id, descending
    matches_requested=<n>          # Maximum is 25 matches (default is 25)
    tournament_games_only=<string> # set to only show tournament games
    '''
    parameters = {}
    if not hero_id is None:
        parameters['hero_id'] = hero_id
    if not game_mode is None:
        parameters['game_mode'] = game_mode
    if not skill is None:
        parameters['skill'] = skill
    if not min_players is None:
        parameters['min_players'] = min_players
    if not account_id is None:
        parameters['account_id'] = account_id
    if not league_id is None:
        parameters['league_id'] = league_id
    if not start_at_match_id is None:
        parameters['start_at_match_id'] = start_at_match_id
    if not matches_requested is None:
        parameters['matches_requested'] = matches_requested
    if not tournament_games_only is None:
        parameters['tournament_games_only'] = tournament_games_only
    api_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/'
    result = get_valve_web_result(api_url, parameters)
    return result


def get_match_details(match_id):
    '''
    match_id=<id> # the match's ID
    '''
    api_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v001/'
    parameters = {
        'match_id': match_id
    }
    result = get_valve_web_result(api_url, parameters)
    return result


def get_heroes():
    api_url = 'https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/'
    parameters = {}
    result = get_valve_web_result(api_url, parameters)
    return result


def get_player_summaries():
    api_url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    parameters = {}
    result = get_valve_web_result(api_url, parameters)
    return result


def economy_schema():
    api_url = 'https://api.steampowered.com/IEconItems_570/GetSchema/v0001/'
    parameters = {}
    result = get_valve_web_result(api_url, parameters)
    return result


def get_league_listing():
    api_url = 'https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/'
    parameters = {}
    result = get_valve_web_result(api_url, parameters)
    return result


def get_live_league_games(league_id=None):
    api_url = 'https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v0001/'
    parameters = {}
    if not league_id is None:
        parameters['league_id'] = league_id
    result = get_valve_web_result(api_url, parameters)
    return result


def get_match_history_by_sequence_num(start_at_match_seq_num=None,
                                      matches_requested=None):
    '''
    start_at_match_seq_num=<id>    # Start the search at the indicated match id, descending
    matches_requested=<n>          # Maximum is 25 matches (default is 25)
    '''
    api_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v0001/'
    parameters = {}
    if not start_at_match_seq_num is None:
        parameters['start_at_match_seq_num'] = start_at_match_seq_num
    if not matches_requested is None:
        parameters['matches_requested'] = matches_requested
    result = get_valve_web_result(api_url, parameters)
    return result


def get_time_info_by_team_id(start_at_team_id=None,
                             teams_requested=None):
    '''
    start_at_team_id  # the ID of the team to start at
    teams_requested   # the number of teams to return (default is 100)
    '''
    api_url = 'https://api.steampowered.com/IDOTA2Match_570/GetTeamInfoByTeamID/v001/'
    parameters = {}
    if not start_at_team_id is None:
        parameters['start_at_team_id'] = start_at_team_id
    if not teams_requested is None:
        parameters['teams_requested'] = teams_requested
    result = get_valve_web_result(api_url, parameters)
    return result


def get_matched_match(match_list, match_id):
    for match in match_list:
        if match['match_id'] == match_id:
            return match
    return None


tower_list = ['Ancient Top', 'Ancient Bottom', 'Bottom Tier 3', 'Bottom Tier 2', 'Bottom Tier 1',
              'Middle Tier 3', 'Middle Tier 2', 'Middle Tier 1', 'Top Tier 3', 'Top Tier 2', 'Top Tier 1']
barrack_list = []

def get_broken_tower(last_tower_state, current_tower_state):
    broken_tower_list = []
    diff_tower_state = last_tower_state ^ current_tower_state
    for tower_index in range(len(tower_list)):
        if not diff_tower_state & pow(2, len(tower_list) - 1 - tower_index) == 0:
            broken_tower_list.append(tower_index)
    return broken_tower_list


def get_broken_barrack_state(last_barrack_state, current_barrack_state):
    broken_barrack_list = []
    diff_barrack_state = last_barrack_state ^ current_barrack_state
    for barrack_index in range(len(barrack_list)):
        if not diff_barrack_state & pow(2, len(barrack_list) - 1 - barrack_index) == 0:
            broken_barrack_list.append(barrack_index)
    return broken_barrack_list


def check_barracks_state(current_matches_from_web, current_matches_from_db):
    radiant_barracks_state_change = get_broken_barrack_state(current_matches_from_db['scoreboard']['radiant']['barracks_state'],
                                                             current_matches_from_web['scoreboard']['radiant']['barracks_state'])
    dire_barracks_state_change = get_broken_barrack_state(current_matches_from_db['scoreboard']['dire']['barracks_state'],
                                                             current_matches_from_web['scoreboard']['dire']['barracks_state'])
    return radiant_barracks_state_change, dire_barracks_state_change


def check_tower_state(current_matches_from_web, current_matches_from_db):
    radiant_tower_state_change = get_broken_tower(current_matches_from_db['scoreboard']['radiant']['tower_state'],
                                                  current_matches_from_web['scoreboard']['radiant']['tower_state'])
    dire_tower_state_change = get_broken_tower(current_matches_from_db['scoreboard']['dire']['tower_state'],
                                                  current_matches_from_web['scoreboard']['dire']['tower_state'])
    return radiant_tower_state_change, dire_tower_state_change


def check_building_state(current_matches_from_web, current_matches_from_db):
    radiant_tower_state_change, dire_tower_state_change = check_tower_state(current_matches_from_web, current_matches_from_db)
    radiant_barracks_state_change, dire_barracks_state_change = check_barracks_state(current_matches_from_web, current_matches_from_db)
    return radiant_tower_state_change, dire_tower_state_change, radiant_barracks_state_change, dire_barracks_state_change


def check_scoreboard(current_matches_from_web, current_matches_from_db):
    finished_matches = []
    new_start_matches = []
    score_changed_matches = []
    score_unchanged_matches = []
    for match in current_matches_from_db:
        matched_match = get_matched_match(current_matches_from_web, match['match_id'])
        if matched_match is None:
            finished_matches.append(match)
        else:
            if matched_match['scoreboard']['radiant']['score'] == match['scoreboard']['radiant']['score'] and \
               matched_match['scoreboard']['dire']['score'] == match['scoreboard']['dire']['score']:
                score_unchanged_matches.append(match)
            else:
                score_changed_matches.append(matched_match)
    for match in current_matches_from_web:
        matched_match = get_matched_match(current_matches_from_db, match['match_id'])
        if matched_match is None:
            new_start_matches.append(match)
    return finished_matches, score_changed_matches, score_unchanged_matches, new_start_matches


def check_roshan(current_matches_from_web, current_matches_from_db):
    kill_roshan_match = []
    for match in current_matches_from_web:
        matched_match = get_matched_match(current_matches_from_db, match['match_id'])
        if matched_match is None:
            continue
        if not match['scoreboard']['roshan_respawn_timer'] == 0 and matched_match['scoreboard']['roshan_respawn_timer'] == 0:
            kill_roshan_match.append(match)
    return kill_roshan_match


def diff_array(last_array, current_array):
    diff = []
    for index in range(len(last_array), len(current_array)):
        diff.append(current_array[index])
    return diff


def update_ban_pick(match_new_state, match_last_state):
    # print match_new_state
    # print match_last_state
    update_info = {}
    try:
        if not match_new_state['scoreboard']['radiant']['picks'] == match_last_state['scoreboard']['radiant']['picks']:
            update_info['radiant_pick'] = diff_array(match_last_state['scoreboard']['radiant']['picks'], match_new_state['scoreboard']['radiant']['picks'])
    except KeyError:
        pass
    try:
        if not match_new_state['scoreboard']['radiant']['bans'] == match_last_state['scoreboard']['radiant']['bans']:
            update_info['radiant_ban'] = diff_array(match_last_state['scoreboard']['radiant']['bans'], match_new_state['scoreboard']['radiant']['bans'])
    except KeyError:
        pass
    try:
        if not match_new_state['scoreboard']['dire']['picks'] == match_last_state['scoreboard']['dire']['picks']:
            update_info['dire_pick'] = diff_array(match_last_state['scoreboard']['dire']['picks'], match_new_state['scoreboard']['dire']['picks'])
    except KeyError:
        pass
    try:
        if not match_new_state['scoreboard']['dire']['bans'] == match_last_state['scoreboard']['dire']['bans']:
            update_info['dire_ban'] = diff_array(match_last_state['scoreboard']['dire']['bans'], match_new_state['scoreboard']['dire']['bans'])
    except KeyError:
        pass
    return update_info


def update_current_matches():
    current_matches_from_web = get_live_league_games(league_id=DAC_LEAGUE_ID)
    if current_matches_from_web.get('result') is None:
        return
    current_matches_from_web = current_matches_from_web['result']['games']
    current_matches_from_db = list(current_matches_collection.find({}))
    # print current_matches_from_web
    # print current_matches_from_db

    try:
        finished_matches, score_changed_matches, score_unchanged_matches, new_start_matches = check_scoreboard(current_matches_from_web, current_matches_from_db)
        print "finished matches : " + str(map(lambda match: match['match_id'], finished_matches))
        print "score changed matches : " + str(map(lambda match: match['match_id'], score_changed_matches))
        print "score unchanged matches : " + str(map(lambda match: match['match_id'], score_unchanged_matches))
        print "new start matches : " + str(map(lambda match: match['match_id'], new_start_matches))
        match_id_list = map(lambda match: match['match_id'], score_changed_matches + score_unchanged_matches)
        print match_id_list
        for match_id in match_id_list:
            ban_pick_update_info = update_ban_pick(get_matched_match(current_matches_from_web, match_id),
                                                   get_matched_match(current_matches_from_db, match_id))
            print "match id : " + str(match_id)
            for (key, value) in ban_pick_update_info.items():
                if not len(value) == 0:
                    print str(key) + " : " + str(value)
            match = get_matched_match(current_matches_from_web, match_id)
            print "radiant score : ", match['scoreboard']['radiant']['score']
            print "dire score : ", match['scoreboard']['dire']['score']
            kill_roshan_match = check_roshan(current_matches_from_web, current_matches_from_db)
            print "match id : " + str(match_id) + "; kill roshan ! : " + str(kill_roshan_match)
            radiant_tower_state_change, dire_tower_state_change, radiant_barracks_state_change, dire_barracks_state_change \
                = check_building_state(get_matched_match(current_matches_from_web, match_id),
                                       get_matched_match(current_matches_from_db, match_id))
            if not len(radiant_tower_state_change) == 0:
                print "match id : " + str(match_id) + "; radiant lost tower : " + str(radiant_tower_state_change) + " !"
            if not len(dire_tower_state_change) == 0:
                print "match id : " + str(match_id) + "; dire lost tower : " + str(dire_tower_state_change) + " !"
            if not len(radiant_barracks_state_change) == 0:
                print "match id : " + str(match_id) + "; radiant lost barracks : " + str(radiant_barracks_state_change) + " !"
            if not len(dire_barracks_state_change) == 0:
                print "match id : " + str(match_id) + "; dire lost barracks : " + str(dire_barracks_state_change) + " !"
    except:
        print "exception!"
    #     pass

    current_matches_collection.remove({})
    for match in current_matches_from_web:
        current_matches_collection.insert(match)

while True:
    update_current_matches()
    time.sleep(10)