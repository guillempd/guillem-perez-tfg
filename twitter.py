import tweepy


def get_api(keys_and_tokens_filename='guillem_keys_and_tokens.txt'):
    with open(keys_and_tokens_filename) as keys_and_tokens_file:
        # Application dependant
        consumer_key = keys_and_tokens_file.readline().rstrip()  # rstrip removes \n from the string
        consumer_secret = keys_and_tokens_file.readline().rstrip()

        # Identified user
        access_token = keys_and_tokens_file.readline().rstrip()
        access_token_secret = keys_and_tokens_file.readline().rstrip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth,
                     retry_count=10,
                     retry_delay=10,
                     retry_errors={401, 404, 500, 503},
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    return api


def main():
    api = get_api('guillem_keys_and_tokens.txt')
    tweets = api.home_timeline()
    print('============================ @', api.me().screen_name, "'s timeline ============================" , sep='')
    print()
    for tweet in tweets:
        print('@', tweet.user.screen_name, ': ', tweet.text, sep='')
        print('-------------------------')


if __name__ == '__main__':
    main()
    exit(0)
