import pymongo
import twitter
import tweepy
import time


def main():
    community_name = 'new_photography'  # TODO change
    celebrity_thres = 1e12  # TODO change
    candidates_users_ids = {'4134545008', '19780878', '365744997', '1603889515', '24550580', '459648135', '1566729828', '2403159697', '314590765', '2227158685', '1229160740', '231160219', '2209457971', '590426634', '1951882837', '65596067', '1360550965', '78592249', '547511821', '2751541633', '1536353779', '2408608069', '1902060313', '555421778', '1384015562', '2541554296', '1313799901', '221501222', '1638480667', '241034692', '2745938725', '2246856880', '61497277', '1227133304', '603619186', '89705185', '270396440', '2698246938', '20474432', '249807875', '176921779', '2207056747', '472326862', '4757869131', '2591068392', '1855754490', '2192863008', '878281200', '556971923', '81972068', '544074029', '1650816818', '1312258850', '297935185', '2329059061', '20623646', '224266373', '49962503', '583678010', '579856783'}
    api = twitter.get_api()
    known_community_users = pymongo.MongoClient()[community_name + '_community'].users
    previous_candidate_sets = pymongo.MongoClient()[community_name + '_community'].sets_initial
    while True:
        previous_candidate_sets.insert_one({'user_list': list(candidates_users_ids)})
        new_candidates_users_ids = set()
        followed_users = []
        for user_id in candidates_users_ids:
            if known_community_users.count({'_id': user_id}):
                friends_ids_str = known_community_users.find_one({'_id': user_id})['friends_ids']
            else:
                print('Downloading friends_ids of user ', user_id, '...', sep='')
                friends_ids = []
                try:
                    for page in tweepy.Cursor(api.friends_ids, user_id=user_id).pages():
                        friends_ids.extend(page)
                        time.sleep(60)
                except tweepy.TweepError:
                    print('Unauthorized access to user', user_id)
                friends_ids_str = []
                for ident in friends_ids:
                    friends_ids_str.append(str(ident))
                known_community_users.insert_one({'_id': user_id, 'friends_ids': friends_ids_str})
            followed_users.extend(friends_ids_str)
        hist = {}  # TODO give another name
        for followed_user in followed_users:
            if followed_user in hist:
                hist[followed_user] += 1
            else:
                hist[followed_user] = 1
        while len(new_candidates_users_ids) < len(candidates_users_ids):
            if not hist:
                break
            else:
                max_followers = 0
                max_user = -1
                for user_id, num_followers in hist.items():
                    if num_followers > max_followers:
                        max_followers = num_followers
                        max_user = user_id
                user = api.get_user(user_id=max_user)
                if not user.followers_count > celebrity_thres and user.friends_count < 100000:
                    new_candidates_users_ids.add(max_user)
                del hist[max_user]
        if new_candidates_users_ids == candidates_users_ids:
            print('--------------COMMUNITY FOUND--------------')
            print(new_candidates_users_ids)
            break
        elif new_candidates_users_ids in map(lambda x: set(x['user_list']), previous_candidate_sets.find()):
            print('!!!!!!!!!!INFINITE LOOP!!!!!!!!!!')
            print('new_candidates_users_ids =', new_candidates_users_ids)
            print('candidates_users_ids =', candidates_users_ids)
            break
        else:
            print(candidates_users_ids)
            candidates_users_ids = new_candidates_users_ids











"""
        else:  # I should manually inspect if the users are from the community to do next iteration
            if set(new_candidates_users_ids) in map(lambda x: set(x['user_list']), previous_candidate_sets.find()):
                print('!!!!!!!!!!INFINITE LOOP!!!!!!!!!!')
            else:
                i = 0
                for user_id in new_candidates_users_ids:
                    user = api.get_user(user_id=user_id)
                    print(i, user.screen_name, user_id in known_community_users_ids)
                    i += 1
                print('new_candidate_users_ids =', new_candidates_users_ids)
                print('EXTRA USERS IF NEEDED')
                for i in range(60):  # Maybe put len(candidate_users_ids)
                    if not hist:
                        break
                    else:
                        max_followers = 0
                        max_user = -1
                        for user_id, num_followers in hist.items():
                            if num_followers > max_followers:
                                max_followers = num_followers
                                max_user = user_id
                        new_candidates_users_ids.append(max_user)
                        user = api.get_user(user_id=max_user)
                        print(i, user.screen_name, max_user in known_community_users_ids, max_user)
                        del hist[max_user]
"""


if __name__ == '__main__':
    main()
    exit(0)