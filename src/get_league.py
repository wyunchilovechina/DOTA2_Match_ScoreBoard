#!/usr/bin/python

import urllib2
import httplib
import json
import time
import pymongo

VALVE_ACCESS_TOKEN = '6FA3B90A9ECFC00FE4FEE4B558F80B5D'
LEAGUE_ID = 2339
conn = pymongo.Connection('localhost',27017)
dota2_db = conn.dota2
league_collection = dota2_db.leagues
match_collection = dota2_db.matches


def get_valve_web_result(url):
    url_read_handle = urllib2.urlopen(url)
    url_read_data = json.loads(''.join(url_read_handle.readlines()))
    print url_read_data
    return url_read_data['result']


def get_match_list_by_league_id_start_match_id(league_id, match_id):
    url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?league_id=' + str(league_id) + \
          '&key=' + VALVE_ACCESS_TOKEN + '&start_at_match_id=' + str(match_id)
    return get_valve_web_result(url)


def get_match_list_by_league_id(league_id):
    url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?league_id=' + str(league_id) + \
          '&key=' + VALVE_ACCESS_TOKEN
    result = get_valve_web_result(url)
    match_list = result['matches']
    while result['results_remaining'] != 0:
        most_early_match = match_list[-1]
        result = get_match_list_by_league_id_start_match_id(league_id, most_early_match['match_id'] - 1)
        match_list.extend(result['matches'])
        time.sleep(1)
    return match_list


def get_match_detail(match_id):
    url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id=' + str(match_id) + '&key=' + VALVE_ACCESS_TOKEN
    while True:
        break_flag = False
        try:
            match_detail = get_valve_web_result(url)
            break_flag = True
        except:
            pass
        if break_flag:
            break
        time.sleep(5)
    return match_detail

# league_collection.insert({"league_id": LEAGUE_ID}, {"$set": {"league_id": LEAGUE_ID, "matches": total_match_list}})
result = league_collection.find_one({"league_id": LEAGUE_ID})
if result is None:
    total_match_list = get_match_list_by_league_id(LEAGUE_ID)
    league_collection.insert({"league_id": LEAGUE_ID, "matches": total_match_list})
else:
    total_match_list = league_collection.find_one({"league_id": LEAGUE_ID})['matches']
# total_match_list = list(set(total_match_list))
print len(total_match_list)
# print total_match_list
# total_match_id_list = list(set(map(lambda match: match['match_id'], total_match_list)))

for match in total_match_list:
    # match_collection.insert({"match_id": match['match_id']}, {"$set": {"match_id": match['match_id'], "detail": match}})
    # match_collection.insert({"match_id": match['match_id'], "detail": match})
    result = match_collection.find_one({"match_id": match['match_id']})
    # print match['match_id']
    # print result
    if result is None:
        print match['match_id']
        match_detail = get_match_detail(match['match_id'])
        match_collection.insert({"match_id": match['match_id'], "detail": match_detail})
        time.sleep(5)
# print total_match_id_list