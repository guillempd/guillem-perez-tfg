import pymongo

import twitter


def main():
    api = twitter.get_api()
    community_name = 'new_photography'  # TODO Modify this for other communities
    community = pymongo.MongoClient()[community_name + '_community']['def_users']  # TODO Modify this for other
    community_dict = {}
    for user in community.find():
        community_dict[user['_id']] = {'friends_ids': user['friends_ids'], 'friends_within_community_ids': [],
                                       'followers_within_community_ids': []}
    community_users = list(community_dict.keys())
    for user_id, user_info in community_dict.items():
        user = api.get_user(user_id=user_id)
        user_info['screen_name'] = user.screen_name
        user_info['verified'] = user.verified
        user_info['followers_count'] = user.followers_count
        user_info['friends_count'] = user.friends_count
        user_info['statuses_count'] = user.statuses_count
        user_info['created_at'] = user.created_at
        friends_ids = user_info['friends_ids']
        friends_within_community_ids = []
        for friend_id in friends_ids:
            if friend_id in community_users:
                friends_within_community_ids.append(friend_id)
        user_info['friends_within_community_ids'] = friends_within_community_ids
        for friend_within_community_id in friends_within_community_ids:
            community_dict[friend_within_community_id]['followers_within_community_ids'].append(user_id)
    for user_id, user_info in community_dict.items():
        user = {'_id': user_id, 'screen_name': user_info['screen_name'], 'verified': user_info['verified'],
                'followers_count': user_info['followers_count'], 'friends_count': user_info['friends_count'],
                'statuses_count': user_info['statuses_count'], 'created_at': user_info['created_at'],
                'friends_ids': user_info['friends_ids'],
                'friends_within_community_ids': user_info['friends_within_community_ids'],
                'followers_within_community_ids': user_info['followers_within_community_ids']}
        community.update({'_id': user_id}, user)


if __name__ == '__main__':
    main()
    exit(0)
