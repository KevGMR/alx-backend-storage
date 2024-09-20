#!/usr/bin/env python3
'''pymongo module
'''


def schools_by_topic(mongo_collection, topic):
    '''returns list of school having a specific topic
    '''
    matched = {
        'topics': {
            '$elemMatch': {'$eq': topic}
        }
    }
    return [item for item in mongo_collection.find(matched)]
