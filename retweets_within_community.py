import pymongo


def main():
    community_name = 'haskell'
    tweets = pymongo.MongoClient()[community_name + '_community'].tweets
    retweets = {}
    for tweet in tweets.find():
        retweets[tweet['_id']] = 0
    for tweet in tweets.find():
        if 'retweeted_id' in tweet:
            if tweet['retweeted_id'] in retweets:
                retweets[tweet['retweeted_id']] += 1
    for tweet in tweets.find():
        tweet['retweet_within_community_count'] = retweets[tweet['_id']]
        tweets.update({'_id': tweet['_id']}, tweet)



if __name__ == '__main__':
    main()
    exit(0)