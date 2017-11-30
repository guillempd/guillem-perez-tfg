import tweepy
import twitter
import pymongo


class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        super(MyStreamListener, self).__init__()
        self.count = 0
        self.collection = pymongo.MongoClient().secondexperiment.randomusers  # Change destiny collection

    def on_status(self, status):
        if self.count < 100:
            n_friends = status.user.friends_count
            n_followers = status.user.followers_count
            if n_friends == 200 and n_followers <= 500:
                self.count += 1
                self.collection.insert_one({'id': status.user.id})
                print(self.count, n_friends)
        else:
            exit(0)


def main():
    api = twitter.get_api()
    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
    my_stream.sample()


if __name__ == '__main__':
    main()
    exit(0)
