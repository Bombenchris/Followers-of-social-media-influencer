import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import numpy as np
from datetime import datetime


def get_ranking(game, n_select):
    game_db = '{}.db'.format(game)
    conn = sqlite3.connect(game_db)
    c = conn.cursor()

    # data id order by follower number desc.
    c.execute('SELECT ID FROM user_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select))
    data = c.fetchall()
    c.close()
    return data


def get_edge(game):

    edge_db = '{}_Edge.db'.format(game)
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()
    edge_list = c.execute("SELECT source,date,target_rank FROM Edges_db ORDER by source,date").fetchall()
    return edge_list


game = 'Overwatch'
edge_list = get_edge(game)
# data = [(100,'2020-04-03T20:11:08Z',1),(100,'2020-04-04T20:11:08Z',2),(121,'2020-04-5T20:11:08Z',3),(121,'2020-04-07T20:11:08Z',1)]

source, timestamp, target_rank = zip(*edge_list)
dates = [datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ') for d in timestamp]

source = np.array(source)
dates = np.array(dates)
score = np.array(target_rank)

fig, ax = plt.subplots()
for id in np.unique(source):     # Loop over all the unique source's id
    pw = np.where(source == id)  # which elements belong to this id
    ax.plot(dates[pw], score[pw], '-x')


ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.autoscale_view()
ax.set_title('matplotlib.axes.Axes.plot_date Example2')
ax.grid(True)
plt.setp(ax.get_xticklabels(), rotation=15)
plt.legend(frameon=False, loc='best')
plt.show()