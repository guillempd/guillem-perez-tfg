import twitter
import pymongo


def common_friends(user_id_a, user_id_b, api):
    friends_a = set(api.friends_ids(user_id=user_id_a))
    friends_b = set(api.friends_ids(user_id=user_id_b))
    friends_in_common = friends_a.intersection(friends_b)
    # all_friends = friends_a.union(friends_b)
    return len(friends_in_common)  # /len(all_friends)


def main():
    api = twitter.get_api()
    random_users = list(pymongo.MongoClient().secondexperiment.randomusers.find())
    results = []
    for i in range(10):
        random_user_id = random_users[2*i]['id']
        random_pair_id = random_users[2*i + 1]['id']
        result = common_friends(random_user_id, random_pair_id, api)
        results.append({'common': result})
        print(result)
    pymongo.MongoClient().secondexperiment.randomresults.insert(results)


if __name__ == '__main__':
    main()
    exit(0)
