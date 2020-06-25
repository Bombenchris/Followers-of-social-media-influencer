import sqlite3
from twitchAPI.twitch import Twitch
from tqdm import tqdm
import sys


class EdgesPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("The Legend of Zelda_Edge.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""create table IF NOT EXISTS Edges_db(
                Source INTEGER,
                Target INTEGER,
                Type TEXT,
                Date TEXT,
                Target_rank INTEGER,
                UNIQUE (Source, Target)
                )""")

    def store_db(self, item):
        self.curr.execute("""insert or replace into Edges_db values (?,?,?,?,?)""", (
            item['SOURCE'],
            item['TARGET'],
            item['TYPE'],
            item['DATE'],
            item['RANK']
        ))
        self.conn.commit()

    def follower_parse(self, user_id, rank, loops):
        edgePage_cursor = []

        for loop in range(loops):
            if not edgePage_cursor:
                user_followers = twitch.get_users_follows(first=100, to_id=user_id)
                try:
                    edgePage_cursor.append(user_followers['pagination']['cursor'])
                except:
                    pass
            else:
                user_followers = twitch.get_users_follows(after=edgePage_cursor.pop(), first=100, to_id=user_id)

                try:
                    edgePage_cursor.append(user_followers['pagination']['cursor'])
                except:
                    pass

            items = {}
            for follower in user_followers['data']:
                items['SOURCE'] = int(follower['from_id'])
                items['TARGET'] = int(user_id)
                items['TYPE'] = 'Directed'
                items['DATE'] = follower['followed_at']
                items['RANK'] = rank
                self.store_db(items)
        # if edgePage_cursor and 'cursor' in twitch.get_users_follows(after=edgePage_cursor[0], first=100, to_id=user_id)[
        #     'pagination']:
        #     self.follower_parse(user_id, rank, edgePage_cursor)

    def followee_parse(self, user_id, edgePage_cursor):
        if not edgePage_cursor:
            user_followees = twitch.get_users_follows(first=100, from_id=user_id)
            try:
                edgePage_cursor.append(user_followees['pagination']['cursor'])
            except:
                pass
        else:
            user_followees = twitch.get_users_follows(after=edgePage_cursor.pop(), first=100, from_id=user_id)
            try:
                edgePage_cursor.append(user_followees['pagination']['cursor'])
            except:
                pass

        items = {}
        for followee in user_followees['data']:
            items['SOURCE'] = int(user_id)
            items['TARGET'] = int(followee['to_id'])
            items['TYPE'] = 'Directed'
            items['DATE'] = followee['followed_at']
            self.store_db(items)
        if edgePage_cursor and 'cursor' in \
                twitch.get_users_follows(after=edgePage_cursor[0], first=100, from_id=user_id)['pagination']:
            self.followee_parse(user_id, edgePage_cursor)


iMaxStackSize = 10000
sys.setrecursionlimit(iMaxStackSize)

twitch = Twitch('x5chjai5leju0kgmqu4fh8l6hc5ycu', 'csopzwzqls7ogl2e35jvjm089gbyth')
twitch.authenticate_app([])

database = 'The Legend of Zelda.db'
conn = sqlite3.connect(database)
curr = conn.cursor()
n_select = 212
curr.execute('SELECT * FROM user_db ORDER BY FOLLOWERS ASC LIMIT {}'.format(n_select))
data = curr.fetchall()
Pineline = EdgesPipeline()

rank = n_select #descending order, Note: it should be total num. of the database!!!

for row in tqdm(data):
    id = str(row[0])
    follower = row[2]
    loops = round(follower/100) + 1
    print(loops)


    Pineline.follower_parse(id, rank, loops)
    rank -= 1 #ascending order

    # Pineline.followee_parse(id, cursee)
