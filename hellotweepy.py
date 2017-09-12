import tweepy

with open('keys_and_tokens.txt') as file:
    # Application dependant
    consumer_key = file.readline().rstrip() # to remove \n
    consumer_secret = file.readline().rstrip()

    # Identified user
    access_token = file.readline().rstrip()
    access_token_secret = file.readline().rstrip()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

api.update_status('Hello world!')
