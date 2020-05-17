import sqlite3
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def read_from_db(curr, n_select):
    curr.execute('SELECT COUNT(USER) FROM bilibili_db')
    n = curr.fetchone()[0]  # total number of user
    # n_select = 20
    curr.execute('SELECT * FROM bilibili_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select))
    data = curr.fetchall()
    user_sort = range(1, n_select + 1)
    follower_num = []
    for row in data:
        follower_num.append(row[1])
    return user_sort, follower_num, n


def data_plot(curr, n_select):
    USER_SORT, FOLLOWER_NUM, N = read_from_db(curr, n_select)
    log_USER_SORT = np.log(USER_SORT)
    log_FOLLOWER_NUM = np.log(FOLLOWER_NUM)
    pearson_coeff, p_value = stats.pearsonr(log_USER_SORT, log_FOLLOWER_NUM)

    LR_model = np.polyfit(log_USER_SORT, log_FOLLOWER_NUM, deg=1)
    slope_log, intercept_log = LR_model
    FOLLOWER_predict = np.poly1d(LR_model)
    FOLLOWER_NUM_LP = np.exp(FOLLOWER_predict(log_USER_SORT))

    plt.loglog(USER_SORT, FOLLOWER_NUM, 'o', markersize=2, label='log-log')
    line_fit = plt.loglog(USER_SORT, FOLLOWER_NUM_LP,
                          label="k={:.2f}, ".format(slope_log) + 'coeff={:.2f}'.format(pearson_coeff),
                          color='r')
    plt.legend(loc='upper right')
    plt.xlabel('rank')
    plt.ylabel('Followers')
    plt.title(database + '_N={}'.format(N))
    plt.show()
    plt.plot


# database = 'bilibili_douga_other_01012020_01042020.db'
database = 'bilibili_ent_star_01012020_01042020.db'
conn = sqlite3.connect(database)

c = conn.cursor()
n_select = 2000
data_plot(c, n_select)
