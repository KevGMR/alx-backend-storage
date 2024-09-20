#!/usr/bin/env python3
'''pymongo module
'''


def update_topics(mongo_collection, name, topics):
    '''Changes all topics of a document
    based on name
    '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
