import pymongo
import csv


def main():
    community_name = 'haskell'
    tweets = pymongo.MongoClient()[community_name + '_community'].tweets
    with open(community_name + '_data.csv', 'w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['retweets', 'retweets_within_community'])
        for tweet in tweets.find():
            if 'retweeted_id' not in tweet:
                csvwriter.writerow([tweet['retweet_count'], tweet['retweet_within_community_count']])


if __name__ == '__main__':
    main()
    exit(0)
