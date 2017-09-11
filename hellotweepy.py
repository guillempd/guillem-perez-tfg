import tweepy

with open('keys_and_tokens.txt') as file:
    consumer_key = file.readline().rstrip() # to remove \n
    consumer_secret = file.readline().rstrip()

    access_token = file.readline().rstrip()
    access_token_secret = file.readline().rstrip()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

username = 'guillemp95' # username is not case sensitive
user = api.get_user(username)
print(username, 'has', user.followers_count, 'followers and', user.friends_count, 'friends.')
