import sqlite3
import matplotlib.pyplot as plt


def get_filter_edge(edge_db, n_least):
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()
    total_edge = c.execute("SELECT source,COUNT(*) FROM Edges_db GROUP BY source").fetchall()
    OutputList = list(filter(lambda x: x[1] >= n_least, total_edge))  # filter out edge
    OutputList = tuple(edge for (edge, n) in OutputList)
    insert_edge = c.execute("SELECT * FROM Edges_db where Source in {}".format(OutputList)).fetchall()
    c.close()

    return insert_edge


def get_filter_num(edge_db, cons):
    filter_edge_num = []
    filter_node_num = []
    conn = sqlite3.connect(edge_db)
    c = conn.cursor()
    total_edge = c.execute("SELECT source,COUNT(*) FROM Edges_db GROUP BY source").fetchall()
    for n_least in cons:
        OutputList = list(filter(lambda x: x[1] >= n_least, total_edge))  # filter out edge
        edgeSum = list(n for (edge, n) in OutputList)
        nodeSum = len(OutputList)
        filter_edge_num.append(sum(edgeSum))
        filter_node_num.append(nodeSum)
    c.close()

    return filter_edge_num, filter_node_num


def write_to_edgeDB(game, n_least, total_id, insert_edge):
    # insert to a new database file
    edge_filter_db = '{}_Edge_filter{}.db'.format(game, n_least)
    conn = sqlite3.connect(edge_filter_db)
    c = conn.cursor()
    createTable = """CREATE TABLE IF NOT EXISTS Edges_db(Source INTEGER,
                    Target INTEGER,
                    Type TEXT,
                    Date TEXT
                    )"""
    c.execute(createTable)
    insertTable = "INSERT or ignore INTO Edges_db values (?,?,?,?)"
    c.executemany(insertTable, insert_edge)
    conn.commit()

    # Count the followers number for each Target
    total_follower = c.execute(
        "SELECT Target,COUNT(*) FROM Edges_db WHERE target IN {} GROUP BY Target".format(total_id)).fetchall()
    c.close()
    return total_follower


def write_to_gameDB(game, n_least, total_follower):
    # group follower number, rewrite to database
    follower_filter_db = '{}_filter{}.db'.format(game, n_least)
    conn = sqlite3.connect(follower_filter_db)
    c = conn.cursor()
    createTable = """CREATE TABLE IF NOT EXISTS user_db(
                    Id INTEGER UNIQUE,
                    FOLLOWERS INTEGER
                    )"""
    c.execute(createTable)
    insertTable = "INSERT or ignore INTO user_db values (?,?)"
    c.executemany(insertTable, total_follower)
    conn.commit()
    c.close()


def get_rank(game, n_select, filter_range):
    Id = []
    nodes = list(range(n_select))
    rank = [[] for _ in range(n_select)]
    follower_filter = [[] for _ in range(n_select)]

    for fq_filter in filter_range:
        if fq_filter > 1:
            game_db = '{}_filter{}.db'.format(game, fq_filter)  # test
        else:
            game_db = '{}.db'.format(game)

        conn = sqlite3.connect(game_db)
        c = conn.cursor()
        if not Id:
            Id = c.execute('SELECT ID FROM user_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select)).fetchall()

        data = c.execute("SELECT * FROM user_db ORDER by followers DESC").fetchall()
        for node in nodes:
            id = Id[node][0]
            id_rank = [y[0] for y in data].index(id) + 1
            if fq_filter > 1:
                follower_nr = [t[1] for t in data if t[0] == id].pop()
            else:
                follower_nr = [t[2] for t in data if t[0] == id].pop()
            rank[node].append(id_rank)
            follower_filter[node].append(follower_nr)
    return rank, follower_filter


game = 'Minecraft Dungeons'
edge_db = '{}_Edge_list.db'.format(game)  # Load Edge list

# # create the filtered database
# conn = sqlite3.connect('{}.db'.format(game))
# c = conn.cursor()
# total_id = c.execute("SELECT id FROM user_db ").fetchall()
# total_id = tuple(id[0] for id in total_id)
# c.close()
# for n_least in range(2, 9):
#     insert_edge = get_filter_edge(edge_db, n_least)
#     total_follower = write_to_edgeDB(game, n_least, total_id, insert_edge)
#     write_to_gameDB(game, n_least, total_follower)

# plot the trajectory of ranking
n_select = 20
filter_range = list(range(1, 6))
rank, follower_filter = get_rank(game, n_select, filter_range)
fig, ax = plt.subplots()
for row in rank:
    ax.plot(filter_range, row, 'o-')

plt.xlabel('threshold k')
plt.ylabel('Rank')
plt.title('{}_ranking trajectory for top node'.format(game))

fig, ax = plt.subplots()
for row in follower_filter:
    ax.loglog(filter_range, row, 'o-')
plt.xlabel('threshold k')
plt.ylabel('Follower')
plt.title('{}_Folllower trajectory for top node'.format(game))
plt.show()

# plot edge and node number by filtering.
freq = list(range(1, 10))
filter_edge_num, filter_node_num = get_filter_num(edge_db, freq)

plt.figure(0)
plt.loglog(freq, filter_edge_num, 'o-', color='r', label='Total edge')
plt.legend(loc='upper right')
plt.xlabel('threshold k')
plt.ylabel('Nr.Edges')
plt.title('{} Edges by filtering'.format(game))

plt.figure(1)
plt.loglog(freq, filter_node_num, 'o-', color='k', label='Total node')
plt.legend(loc='upper right')
plt.xlabel('threshold k')
plt.ylabel('Nr.Nodes')
plt.title('{} Nodes by filtering'.format(game))

plt.show()
