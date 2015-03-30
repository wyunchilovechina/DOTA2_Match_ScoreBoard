__author__ = 'wyunchi'

import pymongo

conn = pymongo.Connection()
dota2_db = conn.dota2
current_matches_collection = dota2_db.current_matches

hero_collection = dota2_db.heros
item_collection = dota2_db.items
lobby_collection = dota2_db.lobbies
ability_collection = dota2_db.abilibties
match_collection = dota2_db.matches

match_list = map(lambda match: match['detail'], list(match_collection.find()))
# print match_list
hero_list = list(hero_collection.find())

def get_hero_index_by_id(id):
    for index in range(len(hero_list)):
        if hero_list[index]['id'] == id:
            return index
    return None

for index in range(len(hero_list)):
    hero = hero_list[index]
    hero['picks'] = 0
    hero['bans'] = 0
    hero['kills'] = 0
    hero['deaths'] = 0
    hero['assists'] = 0
    hero['hero_healing'] = 0
    hero['hero_damage'] = 0
    hero_list[index] = hero

# a = map(lambda x: x['match_id'], filter(lambda y: not (y.has_key('picks_bans') and y['lobby_type'] == 1 and y['human_players'] == 10), match_list))
# for match_id in a:
#     match_collection.remove({"match_id": match_id})


for match in match_list:
    picks_bans = match['picks_bans']
    # try:
    #     picks_bans = match['picks_bans']
    # except KeyError:
    #     # print match
    #     break
    players = match['players']
    for bp in picks_bans:
        hero_index = get_hero_index_by_id(bp['hero_id'])
        if hero_index is None:
            print "can not find hero : " + str(bp)
        else:
            if bp['is_pick']:
                hero_list[hero_index]['picks'] += 1
            else:
                hero_list[hero_index]['bans'] += 1

    for player in players:
        hero_index = get_hero_index_by_id(player['hero_id'])
        if hero_index is None:
            print "can not find hero : " + str(player['hero_id'])
        else:
            hero_list[hero_index]['kills'] += player['kills']
            hero_list[hero_index]['deaths'] += player['deaths']
            hero_list[hero_index]['assists'] += player['assists']
            hero_list[hero_index]['hero_healing'] += player['hero_healing']
            hero_list[hero_index]['hero_damage'] += player['hero_damage']

print hero_list