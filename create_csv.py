import csv
import pymongo


def main():
    community_name = 'new_photography'  # TODO Modify for other communities
    community = pymongo.MongoClient()[community_name + '_community']['def_users']  #TODO Modify for other communities
    with open(community_name + '_nodes.csv', 'w') as nodes_file:
        fieldnames = ['_id', 'screen_name', 'verified', 'followers_count', 'friends_count', 'statuses_count',
                      'created_at']
        writer = csv.DictWriter(nodes_file, fieldnames=fieldnames, dialect='excel-tab', extrasaction='ignore')
        writer.writeheader()
        for user in community.find():
            writer.writerow(user)

    with open(community_name + '_edges.csv', 'w') as edges_file:
        fieldnames = ['user', 'friend']
        writer = csv.DictWriter(edges_file, fieldnames=fieldnames, dialect='excel-tab')
        writer.writeheader()
        for user in community.find():
            for friend in user['friends_within_community_ids']:
                writer.writerow({'user': user['_id'] , 'friend': friend})


if __name__ == '__main__':
    main()
    exit(0)