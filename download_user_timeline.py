import twitter
import pymongo


def store_in_db(tweet, collection):
    row = {"_id": tweet.id,
           "text": tweet.text,
           "user_screen_name": tweet.user.screen_name,  # TODO is this really needed taking into account the structure of the db?
           "user_id": tweet.user.id,  # TODO idem
           "date": tweet.created_at,
           "rt_count": tweet.retweet_count}
    if hasattr(tweet, 'retweeted_status'):
        row['retweeted_id'] = tweet.retweeted_status.id
    collection.insert_one(row)


def main():
    user_id = '204916626'
    api = twitter.get_api()
    collection = pymongo.MongoClient().userstimelines[user_id]
    oldest_tweet_id = -1
    total_retrieved_tweets = 0
    while True:
        if oldest_tweet_id == -1:
            retrieved_tweets = api.user_timeline(user_id=user_id)
        else:
            retrieved_tweets = api.user_timeline(user_id=user_id, max_id=oldest_tweet_id-1)
        n_retrieved_tweets = len(retrieved_tweets)
        print('Retrieved', n_retrieved_tweets, 'tweets.')
        total_retrieved_tweets += n_retrieved_tweets
        if n_retrieved_tweets == 0:
            break
        for tweet in retrieved_tweets:
            store_in_db(tweet, collection)
            if oldest_tweet_id == -1:
                oldest_tweet_id = tweet.id
            elif tweet.id < oldest_tweet_id:
                oldest_tweet_id = tweet.id
    print('Download of user timeline completed,', total_retrieved_tweets, 'retrieved tweets.')


if __name__ == '__main__':
    main()
    exit(0)
