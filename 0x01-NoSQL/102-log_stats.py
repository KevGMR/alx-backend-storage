#!/usr/bin/env python3
'''pymongo module
'''
from pymongo import MongoClient


def nginx_logs(nginx_collections):
    '''Print Nginx HTTP methods logs
    '''
    print('{} logs'.format(nginx_collections.count_documents({})))
    print('Methods:')
    http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in http_methods:
        total_count = len(list(nginx_collections.find({'method': method})))
        print('\tmethod {}: {}'.format(method, total_count))
    status_count = len(list(nginx_collections.find(
        {'method': 'GET', 'path': '/status'}
    )))
    print('{} status check'.format(status_count))
    print('IPs:')
    ips = nginx_collections.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in ips:
        top_ip = ip.get("ip")
        count = ip.get("count")
        print('\t{}: {}'.format(top_ip, count))


def start_db():
    '''connects to db client and run above function
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs(client.logs.nginx)


if __name__ == '__main__':
    start_db()
