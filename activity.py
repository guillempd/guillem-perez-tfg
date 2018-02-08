from datetime import date

import twitter


def activity(screen_name, api):
    user = api.get_user(screen_name)

    n_tweets = user.statuses_count

    register_date = user.created_at.date()
    today_date = date.today()
    days_since_register = (today_date - register_date).days

    activity = n_tweets / days_since_register  # in tweets/day
    # print('n_tweets =', n_tweets)
    # print('days_since_register =', days_since_register)
    return activity



def main():
    api = twitter.get_api()
    screen_names = ['ERC_elvendrell', 'cristian_agudo', 'uripir', 'DUMICO_10', 'JosepBargallo', 'alfonsjm']
    for screen_name in screen_names:
        print(screen_name, activity(screen_name, api))


if __name__ == '__main__':
    main()
    exit(0)