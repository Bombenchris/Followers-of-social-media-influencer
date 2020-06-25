import sqlite3
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import numpy as np
from datetime import datetime


def get_edge(game, timewindows):
    database = '{}.db'.format(game)
    conn = sqlite3.connect(database)
    curr = conn.cursor()
    n_select = 50
    broadcaster = curr.execute('SELECT * FROM user_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select)).fetchall()
    broadcaster = tuple(row[0] for row in broadcaster)

    edge_db = '{}_Edge.db'.format(game)
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()
    user = c.execute("SELECT source FROM Edges_db GROUP by source HAVING COUNT(target) >= 3").fetchall()
    user = tuple(edge[0] for edge in user)

    # user = c.execute("SELECT DISTINCT source FROM Edges_db where target in {} ORDER by source,date".format(broadcaster)).fetchall()
    # user = tuple(row[0] for row in user)

    edge_list = c.execute(
        "SELECT source,date,target_rank FROM Edges_db where source in {} and '{}'<=date and date<='{}' ORDER by source,date".format(
            user, timewindows[0], timewindows[1])).fetchall()
    return edge_list


def re_ranking(game, timewindows):
    edge_db = '{}_Edge.db'.format(game)
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()
    target_list = c.execute(
        "SELECT target FROM Edges_db where '{}'<=date and date<='{}' GROUP by target ORDER BY COUNT(source) DESC".format(
            timewindows[0], timewindows[1])).fetchall()
    new_rank = 0
    for target in target_list:
        new_rank += 1
        c.execute("update Edges_db set target_rank = {} where target = {}".format(new_rank, target[0]))
        conn.commit()


game = 'The Legend of Zelda'

# re_ranking(game, timewindows=["2020-05-01", "2020-07-01"])

edge_list = get_edge(game, timewindows=["2020-05-01", "2020-06-15"])

source, timestamp, target_rank = zip(*edge_list)
dates = [datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ') for d in timestamp]

source = np.array(source)
dates = np.array(dates)
score = np.array(target_rank)

fig, ax = plt.subplots()
for id in np.unique(source):  # Loop over all the unique source's id
    pw = np.where(source == id)  # which elements belong to this id
    ax.plot(dates[pw], score[pw], '-x')

ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.autoscale_view()
ax.set_title('{} follower dynamics Outdegree>=3 '.format(game))
ax.grid(True)
plt.setp(ax.get_xticklabels(), rotation=15)
plt.legend(frameon=False, loc='best')
plt.ylabel('Ranking')
plt.show()
