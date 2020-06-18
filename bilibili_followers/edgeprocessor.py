import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmap


def get_data(game, n_select, fq_filter):
    if fq_filter > 1:
        game_db = '{}_filter{}.db'.format(game, fq_filter)  # test
    else:
        game_db = '{}.db'.format(game)

    conn = sqlite3.connect(game_db)
    c = conn.cursor()

    # data id order by follower number desc.
    c.execute('SELECT ID FROM user_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select))
    data = c.fetchall()
    c.close()

    return data, game_db


def filter_heatmap(game, data, t, fq_filter, n_select):
    data_filter = []
    if fq_filter > 1:
        edge_db = '{}_Edge_filter{}.db'.format(game, fq_filter)
    else:
        edge_db = '{}_Edge_list.db'.format(game)
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()
    source_first = c.execute("SELECT source FROM Edges_db WHERE target = {}".format(data[0][0])).fetchall()
    source_first = set(source_first)
    for i in range(n_select):
        source_i = c.execute("SELECT source FROM Edges_db WHERE target = {}".format(data[i][0])).fetchall()
        source_i = set(source_i)
        overlap = len(source_first & source_i) / len(source_i)
        if overlap >= t:
            data_filter.append(data[i])
    return data_filter


def create_heatmap(game, data, fq_filter):
    heatmap = []
    n_select = len(data)
    label_xy = list(range(1, n_select + 1))
    if fq_filter > 1:
        edge_db = '{}_Edge_filter{}.db'.format(game, fq_filter)
    else:
        edge_db = '{}_Edge_list.db'.format(game)
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()

    for i in range(n_select):
        row_i = []
        source_i = c.execute("SELECT source FROM Edges_db WHERE target = {}".format(data[i][0])).fetchall()
        source_i = set(source_i)
        for j in range(n_select):
            source_j = c.execute("SELECT source FROM Edges_db WHERE target = {}".format(data[j][0])).fetchall()
            source_j = set(source_j)
            row_i.append(len(source_j & source_i) / len(source_i))
        heatmap.append(row_i)

    return heatmap, label_xy


game = 'Overwatch'
n_select = 30
fq_filter = 2
user_sort = range(1, n_select + 1)
data, game_db = get_data(game, n_select, fq_filter)
# if fq_filter > 1:
#     edge_db = '{}_Edge_filter{}.db'.format(game, fq_filter)  # test
# else:
#     edge_db = '{}_Edge_list.db'.format(game)
# conn = sqlite3.connect(edge_db)
# c = conn.cursor()
#
# OverlapToRank = 0
# total_edge = c.execute("select count(*) from Edges_db").fetchone()[0]
# # set of followers from rank 1st streamer
# source_first = c.execute("SELECT source FROM Edges_db WHERE target = {}".format(data[OverlapToRank][0])).fetchall()
# source_first = set(source_first)
#
# marker = itertools.cycle(('o', '+', 'x', '*', '.', 'X'))
# date = ['2018-06-01', '2018-12-01', '2019-06-01', '2019-12-01', '2020-06-02']
# for time in date:
#     Followers = []
#     Intersection = []
#     for id in data:
#         c.execute("SELECT COUNT(*) FROM Edges_db WHERE target = {} and DATE <= '{}'".format(id[0], time))
#         n_followers = c.fetchone()
#         Followers.append(n_followers[0])
#
#         if time == date[-1]:
#             source_id = c.execute("SELECT source FROM Edges_db WHERE target = {}".format(id[0])).fetchall()
#             source_id = set(source_id)
#             Intersection.append(len(source_first & source_id))
#
#     plt.figure(0)
#     plt.loglog(user_sort, Followers, marker=next(marker), label=time)
#     if time == date[-1]:
#         log_USER_SORT = np.log(user_sort)
#         log_FOLLOWER_NUM = np.log(Followers)
#         pearson_coeff, p_value = stats.pearsonr(log_USER_SORT, log_FOLLOWER_NUM)
#         LR_model = np.polyfit(log_USER_SORT, log_FOLLOWER_NUM, deg=1)
#         slope_log, intercept_log = LR_model
#         FOLLOWER_predict = np.poly1d(LR_model)
#         FOLLOWER_NUM_LP = np.exp(FOLLOWER_predict(log_USER_SORT))
#         plt.loglog(user_sort, FOLLOWER_NUM_LP, '--',
#                    label="k={:.2f}, ".format(slope_log) + 'coeff={:.2f}'.format(pearson_coeff),
#                    color='k')
#
# plt.legend(loc='upper right')
# plt.xlabel('rank')
# plt.ylabel('Followers')
# plt.title(game_db + '_Loglog_N_select={} and N_edge={}'.format(n_select, total_edge))

# Percent = [intersect / Followers[OverlapToRank] for intersect in Intersection]
# # Percent = [x / y for x, y in zip(Intersection, Followers)]
# plt.figure(1)
# plt.bar(user_sort, Percent)
# plt.xlabel('rank')
# plt.ylabel('Overlap %')
# plt.title(game_db + '_N_select={} and N_edge={}'.format(n_select, total_edge))

# plot the heatmap
t = 0.5  # threshold for overlap
data_filter = filter_heatmap(game, data, t, fq_filter, n_select)
heatmap, label_xy = create_heatmap(game, data, fq_filter)
heatmap_filter, label_xy_filter = create_heatmap(game, data_filter, fq_filter)
fig, ax = plt.subplots()
plt.imshow(heatmap, cmap=cmap.hot)
plt.colorbar()
# We want to show all ticks...
ax.set_xticks(np.arange(n_select))
ax.set_yticks(np.arange(n_select))
# ... and label them with the respective list entries
ax.set_xticklabels(label_xy)
ax.set_yticklabels(label_xy)
ax.set_title("Overlap fq>={} #followers(i ∩ j) /#followers(i)".format(fq_filter))
fig.tight_layout()
plt.show()

fig2, ax2 = plt.subplots()
plt.imshow(heatmap_filter, cmap=cmap.hot)
plt.colorbar()
# We want to show all ticks...
len_x_2 = len(data_filter)
len_y_2 = len_x_2
ax2.set_xticks(np.arange(len_x_2))
ax2.set_yticks(np.arange(len_y_2))
# ... and label them with the respective list entries
ax2.set_xticklabels(label_xy_filter)
ax2.set_yticklabels(label_xy_filter)
ax2.set_title("Overlap fq>={} #followers(i ∩ j) /#followers(i)".format(fq_filter))
fig2.tight_layout()
plt.show()
