import pymongo


def main():
    community_name = 'new_photography'
    final_set = {'8766122', '2241921', '16295907', '53964666', '15916383', '19181276', '255567998', '191279678', '49356966', '45877354', '22574003', '90918062', '24139054', '18691824', '173661406', '195176644', '14677919', '592846743', '191750596', '104351269', '807095', '133541056', '20546557', '43544315', '302889927', '69300614', '108171720', '6184372', '103630698', '381646547', '16928541', '6184392', '16074111', '28856675', '633726625', '60037975', '24865602', '22411875', '16065736', '41814686', '117662694', '57315608', '136018565', '23179472', '44698296', '258003282', '130540077', '36943525', '19988587', '72499513', '63345416', '86381256', '16401294', '16701822', '247416563', '241109716', '20802277', '32496803', '17471979', '16301072'}
    intermediate_sets = pymongo.MongoClient()[community_name + '_community']['sets_nt']
    users = pymongo.MongoClient()[community_name + '_community'].users
    union_users = pymongo.MongoClient()[community_name + '_community']['def_nt_union_users']

    for intermediate_set in map(lambda x: x['user_list'],intermediate_sets.find()):
        final_set = final_set.union(intermediate_set)
    for user_id in final_set:
        user = users.find_one({'_id': user_id})
        union_users.insert_one(user)


if __name__ == '__main__':
    main()
    exit(0)
