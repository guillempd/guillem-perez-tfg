import twitter
import numpy as np


def main():
    api = twitter.get_api()
    core_users = [14336062, 2904896141, 84053338, 710827859124871168, 31416615, 363696047]
    n_members = 100
    candidates = set()
    for core_user in core_users:
        candidates = candidates.union(set(api.followers_ids(user_id=core_user)))
    candidates = list(candidates)
    print(len(candidates))
    print(list(np.random.choice(candidates, n_members, replace=False)))


if __name__ == '__main__':
    main()
    exit(0)