import pymongo

community_name = 'ai'
thres = 40

def print_screen_name(user_id):
    users = pymongo.MongoClient()[community_name + '_community'].users
    user = users.find_one({'_id': user_id})
    screen_name = user['screen_name']
    print(screen_name, end='')
    if len(user['followers_within_community_ids']) >= thres:
        print('(*)', end='')


def main():
    chain_length = 2
    total_chains = 0
    starting_star_chains = 0
    tweets = pymongo.MongoClient()[community_name + '_community'].tweets
    for tweet in tweets.find({'retweet_within_community_count': chain_length}):
    # AI for tweet in tweets.find({'user_id': {'$ne': '393033324'} , 'retweet_within_community_count': chain_length}):
        total_chains += 1
        chain = tweets.find({'retweeted_id': tweet['_id']})
        chain = list(chain)
        for i in range(len(chain)):
            chain[i] = (chain[i]['created_at'], chain[i]['user_id'])
        chain.sort()
        print('-----------------------------')
        print(tweet['text'])
        print_screen_name(tweet['user_id'])
        users = pymongo.MongoClient()[community_name + '_community'].users
        user = users.find_one({'_id': tweet['user_id']})
        if len(user['followers_within_community_ids']) >= thres:
            starting_star_chains += 1
        for (_, user_id) in chain:
            print(' -> ', end='')
            print_screen_name(user_id)
        print()
    if total_chains > 0:
        print('total_chains =', total_chains)
        print('starting_star_chains =', starting_star_chains)
        print(1 - starting_star_chains/total_chains)

if __name__ == '__main__':
    main()
    exit(0)