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


def delete_nonactive_follower(game, date):

    # get active followers
    edge_db = '{}_Edge.db'.format(game)
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()
    source_active = c.execute("select source from Edges_db where date>'{}' group by source".format(date)).fetchall()
    source_active = tuple(id[0] for id in source_active)
    data_active = c.execute("select * from Edges_db where source in {}".format(source_active)).fetchall()
    c.close()


    # write to new database
    edge_filter_db = '{}_Edge_active.db'.format(game)
    conn = sqlite3.connect(edge_filter_db)
    c = conn.cursor()
    createTable = """create table IF NOT EXISTS Edges_db(
                Source INTEGER,
                Target INTEGER,
                Type TEXT,
                Date TEXT,
                Target_rank INTEGER,
                UNIQUE (Source, Target)
                )"""
    c.execute(createTable)

    insertTable = "INSERT or replace INTO Edges_db values (?,?,?,?,?)"
    c.executemany(insertTable, data_active)
    conn.commit()


game = 'Overwatch'
# n_select = 196
fq_filter = 1
# broadcaster_id = get_data(game, n_select, fq_filter)
delete_nonactive_follower(game, date='2020-06-01')

if fq_filter > 1:
    edge_db = '{}_Edge_filter{}.db'.format(game, fq_filter)
else:
    edge_db = '{}_Edge_active.db'.format(game)
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
