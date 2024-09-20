#!/usr/bin/env python3
'''Mongo - Mongoose module
'''


def list_all(mongo_collection):
    '''List all document in a mongo collection
    '''
    return [doc for doc in mongo_collection.find()]
