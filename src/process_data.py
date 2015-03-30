__author__ = 'wyunchi'

import pymongo

conn = pymongo.Connection()
dota2_db = conn.dota2
match_collection = dota2_db.matches
league_collection = dota2_db.leagues

match_list = list(match_collection.find({}))

