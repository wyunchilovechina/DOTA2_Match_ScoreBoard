#!/usr/bin/python

import json

file_path = "../tmp/1207029664.json"
data_path = "../data/"

hero_json = json.load(open(data_path + 'heroes.json'))['heroes']
abilities_json = json.load(open(data_path + 'abilities.json'))['abilities']
item_json = json.load(open(data_path + 'items.json'))['items']
lobbies_json = json.load(open(data_path + 'lobbies.json'))['lobbies']

# print str(lobbies_json)


def get_hero_name_by_id(id):
    for hero in hero_json:
        if hero['id'] == id:
            return hero['localized_name']


def get_item_name_by_id(id):
    for item in item_json:
        if item['id'] == id:
            return item['name']


def get_ability_name_by_id(id):
    for ability in abilities_json:
        if ability['id'] == id:
            return ability['name']


def process_match_json(match_json):
    player_list = match_json['players']
    for index in range(len(player_list)):
        player = player_list[index]
        player['hero_localized_name'] = get_hero_name_by_id(player['hero_id'])
        player_list[index] = player
        ability_upgrades_list = player['ability_upgrades']
        for ability_index in range(len(ability_upgrades_list)):
            ability = ability_upgrades_list[ability_index]
            ability['ability'] = get_ability_name_by_id(str(ability['ability']))
            ability_upgrades_list[ability_index] = ability
        player['ability_upgrades'] = ability_upgrades_list
        for item_index in range(6):
            player['item_' + str(item_index)] = get_item_name_by_id(player['item_' + str(item_index)])
    match_json['players'] = player_list
    return match_json

match_json = json.load(open(file_path))['result']

match_json = process_match_json(match_json)
print match_json