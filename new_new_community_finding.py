import pymongo
import twitter
import tweepy
import time


def main():
    community_name = 'new_photography'  # TODO change
    candidates_users_ids = {'20431922', '3704442256', '941158676420739072', '47797211', '333805692', '117662694', '952901164416290816', '21850078', '920610521459712000', '787124130948710400', '970308314', '36836023', '473312742', '37971731', '19208551', '458597583', '237483035', '210489589', '19162549', '41814686', '604849323', '23947219', '941826154759061504', '10422602', '1567667966', '29452677', '1450050433', '20785288', '101154711', '3244806647', '300919974', '732636480', '2873738298', '110230887', '231425452', '40297195', '955551308727177216', '41328650', '274746287', '1480316444', '75786254', '939655931968806912', '570954372', '903224812843171840', '714670851396907009', '156864049', '937058501586595840', '1274445318', '327842836', '770326643059613696', '2341897753', '15275022', '955446979579953152', '351001143', '955275979357745152', '14305530', '22411875', '20802277', '16065736', '23179472'}

    api = twitter.get_api()
    known_community_users = pymongo.MongoClient()[community_name + '_community'].users
    previous_candidate_sets = pymongo.MongoClient()[community_name + '_community'].sets_ratio
    while True:
        previous_candidate_sets.insert_one({'user_list': list(candidates_users_ids)})
        # known_community_users_ids = list(map(lambda x: x['_id'], known_community_users.find()))
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
        new_candidates_list = []
        while len(new_candidates_list) < 3*len(candidates_users_ids):
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
                if user.friends_count < 100000:
                    new_candidates_list.append((max_followers/user.followers_count, max_user))
                del hist[max_user]
        new_candidates_list.sort()
        new_candidates_users_ids = set(map(lambda x: x[1], new_candidates_list[-len(candidates_users_ids):]))
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