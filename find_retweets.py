import twitter
import tweepy
import pymongo


def main():
    status_id = 935979683631394816
    user_id = 344395626
    api = twitter.get_api()
    user = api.get_user(user_id=user_id)
    n_followers = user.followers_count
    followers_ids = []
    cursor = -1
    while True:
        print(cursor)
        result = api.followers_ids(user_id=user_id, cursor=cursor)
        print(result)
        followers_ids += result[0]
        cursor = len(followers_ids) - 1
    print(n_followers)
    print(type(followers_ids))
    print(len(followers_ids))
    print(followers_ids)


if __name__ == '__main__':
    main()
    exit(0)