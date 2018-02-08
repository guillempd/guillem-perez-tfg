import twitter
import pymongo


def main():
    api = twitter.get_api()
    user_id = '204916626'
    n_followers = 22  # TODO determine how to get this number (via api or mongodb)
    tweets = pymongo.MongoClient().userstimelines[user_id].find()
    total_rt = 0
    less_followers_rt = 0
    for tweet in tweets:
        if 'retweeted_id' in tweet:
            total_rt += 1
            original_tweet_followers = api.get_status(tweet['retweeted_id']).user.followers_count
            if original_tweet_followers < n_followers:
                less_followers_rt += 1
    print('less_followers_rt =', less_followers_rt)
    print('total_rt =', total_rt)
    print('less_followers_rt/total_rt =', less_followers_rt/total_rt)


if __name__ == '__main__':
    main()
    exit(0)
