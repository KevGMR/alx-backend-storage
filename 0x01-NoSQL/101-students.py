#!/usr/bin/env python3
'''pymongo module
'''


def top_students(mongo_collection):
    '''Prints average score of students
    '''
    param = [
        {"$project": {"name": "$name", "averageScore": {"$avg": "$topics.score"}}},
        {'$sort': {'averageScore': -1}}
    ]
    result = mongo_collection.aggregate(param)
    return result
