from datetime import date

import twitter


def main():
    api = twitter.get_api()
    user_screen_name = 'selenagomez'

    total_retrieved_tweets = 0
    oldest_tweet_id = -1
    hundredth_tweet = None
    while total_retrieved_tweets < 100:
        if oldest_tweet_id == -1:
            retrieved_tweets = api.user_timeline(screen_name=user_screen_name)
        else:
            retrieved_tweets = api.user_timeline(screen_name=user_screen_name, max_id=oldest_tweet_id - 1)
        n_retrieved_tweets = len(retrieved_tweets)
        print('Retrieved', n_retrieved_tweets, 'tweets.')
        if n_retrieved_tweets == 0:
            break
        if total_retrieved_tweets + n_retrieved_tweets >= 100:
            hundredth_tweet = retrieved_tweets[99-total_retrieved_tweets]
        total_retrieved_tweets += n_retrieved_tweets

    if hundredth_tweet is not None:
        hundredth_tweet_date = hundredth_tweet.created_at.date()
        today_date = date.today()
        activity = 100/(today_date - hundredth_tweet_date).days
        print(activity)
    else:
        print('It does not even have 100 tweets, too low activity')


if __name__ == '__main__':
    main()
    exit(0)