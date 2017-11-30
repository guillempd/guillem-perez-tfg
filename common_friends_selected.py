import twitter
import pymongo


def common_friends(user_id_a, user_id_b, api):
    friends_a = set(api.friends_ids(user_id=user_id_a))
    friends_b = set(api.friends_ids(user_id=user_id_b))
    friends_in_common = friends_a.intersection(friends_b)
    all_friends = friends_a.union(friends_b)
    return len(friends_in_common)/len(all_friends)


def main():
    api = twitter.get_api()
    random_users = list(pymongo.MongoClient().firstexperiment.randomusers.find({}))
    results = []
    size = 0
    i = 600
    while size < 10:
        i += 1
        random_user_id = random_users[i]['id']
        candidates_ids = api.followers_ids(user_id=random_user_id)
        for candidate_id in candidates_ids:
            if random_user_id in api.followers_ids(user_id=candidate_id):
                selected_pair_id = candidate_id
                break
        else:
            continue
        result = common_friends(random_user_id, selected_pair_id, api)
        print(result)
        results.append({'common': result})
        size += 1
    pymongo.MongoClient().firstexperiment.selectedresults.insert(results)


if __name__ == '__main__':
    main()
    exit(0)
