import pymongo
import csv


def main():
    community_name = 'haskell'
    users = pymongo.MongoClient()[community_name + '_community'].users
    followed_users = []
    for user in users.find():
        followed_users.extend(user['friends_ids'])
    hist = {}
    for follow in followed_users:
        if follow in hist:
            hist[follow] += 1
        else:
            hist[follow] = 1
    num_followers = list(hist.values())
    max_followers = max(num_followers)
    followers_hist = [0]*(max_followers + 1)
    for elem in num_followers:
        followers_hist[elem] += 1
    followers_accum = list(followers_hist)
    for i in range(1, max_followers + 1):
        followers_accum[max_followers - i] += followers_accum[max_followers - i + 1]
    with open('C:\\Users\\Guillem\\Google Drive\\Uni\\TFG\\Data\\' + community_name + '_followers.csv', 'w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['num_followers', 'users', 'acc_users'])
        for i in range(1,len(followers_hist)):
            csvwriter.writerow([i, followers_hist[i], followers_accum[i]])


if __name__ == '__main__':
    main()
    exit(0)
