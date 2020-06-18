import sqlite3
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def read_from_db(curr, n_select):
    curr.execute('SELECT COUNT(DISTINCT ID) FROM user_db')
    n = curr.fetchone()[0]  # total number of user

    data_followers = curr.execute('SELECT * FROM user_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select)).fetchall()
    data_views = curr.execute('SELECT * FROM user_db ORDER BY View_count DESC LIMIT {}'.format(n_select)).fetchall()

    user_sort = range(1, n_select + 1)
    follower_num = []
    follower_view_count = []
    rank_view_count = []
    for row in data_followers:
        follower_num.append(row[2])
        follower_view_count.append(row[3])
    for row in data_views:
        rank_view_count.append(row[3])
    return user_sort, follower_num, follower_view_count, rank_view_count, n


def linear_reg_log(x, y):
    pearson_coeff, p_value = stats.pearsonr(x, y)
    LR_model = np.polyfit(x, y, deg=1)
    slope_log, intercept_log = LR_model
    FOLLOWER_predict = np.poly1d(LR_model)
    FOLLOWER_NUM_LP = np.exp(FOLLOWER_predict(x))
    return pearson_coeff, slope_log, intercept_log, FOLLOWER_NUM_LP


def linear_reg(x, y):
    pearson_coeff, p_value = stats.pearsonr(x, y)
    LR_model = np.polyfit(x, y, deg=1)
    slope, intercept = LR_model
    FOLLOWER_predict = np.poly1d(LR_model)
    FOLLOWER_NUM_LP = FOLLOWER_predict(x)
    return pearson_coeff, slope, intercept, FOLLOWER_NUM_LP


def data_plot(curr, n_select):
    USER_SORT, FOLLOWER_NUM, VIEW, RANK_VIEW, N = read_from_db(curr, n_select)
    log_USER_SORT = np.log(USER_SORT)
    log_FOLLOWER_NUM = np.log(FOLLOWER_NUM)
    log_RANK_VIEW = np.log(RANK_VIEW)
    log_VIEW = np.log(VIEW)

    f_pearson_coeff, f_slope_log, f_intercept, FOLLOWER_NUM_LP = linear_reg_log(log_USER_SORT, log_FOLLOWER_NUM)
    v_pearson_coeff, v_slope_log, v_intercept, RANK_VIEW_NUM_LP = linear_reg_log(log_USER_SORT, log_RANK_VIEW)
    fv_pearson_coeff, fv_slope, fv_intercept, FOLLOWER_VIEW_NUM_LP = linear_reg_log(log_FOLLOWER_NUM, log_VIEW)
    # fv_pearson_coeff, fv_slope, fv_intercept, FOLLOWER_VIEW_NUM_LP = linear_reg(FOLLOWER_NUM, VIEW)

    plt.figure(0)
    plt.loglog(USER_SORT, FOLLOWER_NUM, 'o', markersize=2, label='log-log')
    plt.loglog(USER_SORT, FOLLOWER_NUM_LP,
               label="k={:.2f}, ".format(f_slope_log) + 'coeff={:.2f}'.format(f_pearson_coeff),
               color='r')
    plt.legend(loc='upper right')
    plt.xlabel('rank')
    plt.ylabel('Followers')
    plt.title(database + '_N={}'.format(N))

    plt.figure(1)
    plt.loglog(USER_SORT, RANK_VIEW, 'o', markersize=2, label='log-log')
    plt.loglog(USER_SORT, RANK_VIEW_NUM_LP,
               label="k={:.2f}, ".format(v_slope_log) + 'coeff={:.2f}'.format(v_pearson_coeff),
               color='r')
    plt.legend(loc='upper right')
    plt.xlabel('rank')
    plt.ylabel('Views')
    plt.title(database + '_N={}'.format(N))

    plt.figure(2)
    plt.loglog(FOLLOWER_NUM, VIEW, marker='o');
    plt.loglog(FOLLOWER_NUM, FOLLOWER_VIEW_NUM_LP,
             label="k={:.2f} b={:.2f}, ".format(fv_slope, fv_intercept) + 'coeff={:.2f}'.format(fv_pearson_coeff),
             color='r')
    plt.legend(loc='upper right')
    plt.xlabel('Followers')
    plt.ylabel('View')
    plt.title(database + '_N={}'.format(N))
    plt.show()

    plt.plot


# database = 'bilibili_life_funny_01012020_01042020.db'
# database = 'bilibili_music_others_01032020_31032020.db'
# database = 'bilibili_ent_variety_01012020_01042020.db'
# database = 'bilibili_life_funny_01012020_01042020.db'
# database = 'bilibili_movie_montage_01012020_01042020.db'
# database = 'bilibili_ent_star_01012020_01042020.db'
# database = 'bilibili_douga_other_01012020_01042020.db'
database = 'Overwatch.db'  # test
conn = sqlite3.connect(database)
c = conn.cursor()

n_select = [200]
for n in n_select:
    data_plot(c, n)
