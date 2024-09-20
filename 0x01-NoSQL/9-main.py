#!/usr/bin/env python3
'''Python mongoose model
'''


def insert_school(mongo_collection, **kwargs):
    '''insert document to a collection
    '''
    db = mongo_collection.insert_one(kwargs)
    return db.inserted_id
