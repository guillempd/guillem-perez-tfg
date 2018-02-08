import twitter
import pymongo
import tweepy

def store_in_db(tweet, collection):
    row = {'_id': tweet.id_str,
           'text': tweet.text,
           'user_id': tweet.user.id_str,
           'created_at': tweet.created_at,
           'retweet_count': tweet.retweet_count,
           'favorite_count': tweet.favorite_count
           }
    if hasattr(tweet, 'retweeted_status'):
        row['retweeted_id'] = tweet.retweeted_status.id_str
    collection.insert_one(row)


def main():
    api = twitter.get_api()
    community_name = 'new_photography'
    collection = pymongo.MongoClient()[community_name + '_community']['tweets_nt_union']  # TODO
    for user in pymongo.MongoClient()[community_name + '_community']['def_nt_union_users'].find():  # TODO
        user_id = user['_id']
        if not collection.count({'user_id': user_id}):
            oldest_tweet_id = -1
            total_retrieved_tweets = 0
            alt = 0
            while True:
                if oldest_tweet_id == -1:
                    try:
                        retrieved_tweets = api.user_timeline(user_id=user_id)
                    except tweepy.TweepError:
                        print('Couldnt download tweets of', user_id)
                        break
                else:
                    try:
                        retrieved_tweets = api.user_timeline(user_id=user_id, max_id=oldest_tweet_id-1)
                    except tweepy.TweepError:
                        print('Couldnt download tweets of', user_id)
                        break
                n_retrieved_tweets = len(retrieved_tweets)
                print('Retrieved', n_retrieved_tweets, 'tweets.')
                total_retrieved_tweets += n_retrieved_tweets
                if n_retrieved_tweets == 0:
                    break
                for tweet in retrieved_tweets:
                    alt += 1
                    store_in_db(tweet, collection)
                    if oldest_tweet_id == -1:
                        oldest_tweet_id = tweet.id
                    elif tweet.id < oldest_tweet_id:
                        oldest_tweet_id = tweet.id
            print('Download of', user['screen_name'], ' timeline completed,', total_retrieved_tweets, 'tweets retrieved.')
            print(alt)


if __name__ == '__main__':
    main()
    exit(0)
