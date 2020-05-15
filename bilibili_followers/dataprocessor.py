import sqlite3
import matplotlib.pyplot as plt


def read_from_db(curr):
    curr.execute('SELECT * FROM bilibili_db ORDER BY FOLLOWERS DESC')
    data = c.fetchall()
    n = len(data)
    user_sort = range(1, n + 1)
    follower_num = []
    for row in data:
        follower_num.append(row[1])
    return user_sort, follower_num

database = 'bilibili_music_original_01032020_31032020.db'
conn = sqlite3.connect(database)
# conn = sqlite3.connect('bilibili_music_others_01032020_31032020.db')
c = conn.cursor()
USER_SORT, FOLLOWER_NUM = read_from_db(c)
# fig = plt.figure()
# ax = plt.gca()
# ax.scatter(USER_SORT, FOLLOWER_NUM)
# ax.set_yscale('log')
# ax.set_xscale('log')

plt.loglog(USER_SORT, FOLLOWER_NUM, 'o', markersize=2)
plt.xlabel('rank')
plt.ylabel('Followers')
plt.title(database+'_N={}'.format(len(USER_SORT)))
plt.show()

plt.plot