import sqlite3
import numpy as np
import matplotlib.pyplot as plt


def read_from_db(curr):
    curr.execute('SELECT COUNT(DISTINCT USER) FROM bilibili_db')
    n = curr.fetchone()[0]  # total number of user
    n_select = 100
    curr.execute('SELECT * FROM bilibili_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select))
    data = curr.fetchall()
    user_sort = range(1, n_select + 1)
    follower_num = []
    for row in data:
        follower_num.append(row[1])
    return user_sort, follower_num, n


database = 'bilibili_douga_other_01012020_01042020.db'
conn = sqlite3.connect(database)
# conn = sqlite3.connect('bilibili_music_others_01032020_31032020.db')
c = conn.cursor()
USER_SORT, FOLLOWER_NUM, N = read_from_db(c)
log_USER_SORT = np.log(USER_SORT)
log_FOLLOWER_NUM = np.log(FOLLOWER_NUM)

LP_model = np.polyfit(log_USER_SORT, log_FOLLOWER_NUM, deg=1)
slope_log, intercept_log = LP_model
FOLLOWER_predict = np.poly1d(LP_model)
FOLLOWER_NUM_LP = np.exp(FOLLOWER_predict(log_USER_SORT))

plt.loglog(USER_SORT, FOLLOWER_NUM, 'o', markersize=2, label='log-log')
line_fit = plt.loglog(USER_SORT, FOLLOWER_NUM_LP, label="k={:.2f}".format(slope_log), color='r')
plt.legend(loc='upper right')
plt.xlabel('rank')
plt.ylabel('Followers')
plt.title(database + '_N={}'.format(N))
plt.show()

plt.plot
