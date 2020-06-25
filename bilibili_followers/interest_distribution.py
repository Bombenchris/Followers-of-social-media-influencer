import sqlite3
from collections import Counter
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


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

    return data


def delete_id(source, broadcaster_id):
    source = [id for id in source if id not in broadcaster_id]
    return source


game = 'God of War'
n_select = 196
fq_filter = 1
broadcaster_id = get_data(game, n_select, fq_filter)

if fq_filter > 1:
    edge_db = '{}_Edge_filter{}.db'.format(game, fq_filter)
else:
    edge_db = '{}_Edge.db'.format(game)
conn = sqlite3.connect(edge_db)
c = conn.cursor()
source = c.execute("SELECT source FROM Edges_db").fetchall()
# source = delete_id(source, broadcaster_id)

counts = Counter(elem[0] for elem in source)

data = pd.Series(counts)
output = data.value_counts().sort_index()
output.plot(kind='bar', log=True)

plt.xlabel('Follower outdegree')
plt.ylabel('#Follower')
plt.title('{} Nodes outdegree distribution'.format(game))
plt.show()
