import pymongo
import twitter


def main():
    api = twitter.get_api()
    community_name = 'ai'
    community_users = pymongo.MongoClient()[community_name + '_community'].users
    followed_users = []
    community_ids = []
    for user in community_users.find():
        followed_users.extend(user['friends_ids'])
        community_ids.append(user['_id'])
    hist = {}
    for follow in followed_users:
        if follow in hist:
            hist[follow] += 1
        else:
            hist[follow] = 1
    for i in range(100):
        max_followers = 0
        max_user = -1
        for user, followers in hist.items():
            if followers > max_followers:
                max_followers = followers
                max_user = user
        screen_name = api.get_user(user_id=max_user).screen_name
        print(screen_name, max_user in community_ids, max_followers)
        del hist[max_user]


if __name__ == '__main__':
    main()
    exit(0)
