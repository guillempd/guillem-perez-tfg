import time

import pymongo
import tweepy

import twitter


def main():
    users_screen_names = ['BartoszMilewski']

    # TODO Modify this for other communities
    community_name = 'haskell'  # TODO Modify this for other communities
    community = pymongo.MongoClient()[community_name + '_community'].users
    api = twitter.get_api()
    for screen_name in users_screen_names:
        user_id = api.get_user(screen_name=screen_name).id_str
        friends_ids = []
        for page in tweepy.Cursor(api.friends_ids, screen_name=screen_name).pages():
            friends_ids.extend(page)
            print(len(friends_ids))
            print('Sleeping 60 sec')
            time.sleep(60)
        friends_ids_str = []
        for ident in friends_ids:
            friends_ids_str.append(str(ident))
        user = {'_id': user_id, 'screen_name': screen_name, 'friends_ids': friends_ids_str}
        community.insert_one(user)
        print('New user added with', len(friends_ids), 'friends')


if __name__ == '__main__':
    main()
    exit(0)
