import sqlite3
from twitchAPI.twitch import Twitch
from tqdm import tqdm
import sys


class EdgesPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("Overwatch_Edge_list.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""create table IF NOT EXISTS Edges_db(
                Source INTEGER,
                Target INTEGER,
                Type TEXT,
                Date TEXT,
                UNIQUE (Source, Target)
                )""")

    def store_db(self, item):
        self.curr.execute("""insert or ignore into Edges_db values (?,?,?,?)""", (
            item['SOURCE'],
            item['TARGET'],
            item['TYPE'],
            item['DATE']
        ))
        self.conn.commit()

    def follower_parse(self, user_id, edgePage_cursor):
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
            self.store_db(items)
        if edgePage_cursor and 'cursor' in twitch.get_users_follows(after=edgePage_cursor[0], first=100, to_id=user_id)[
            'pagination']:
            self.follower_parse(user_id, edgePage_cursor)

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


iMaxStackSize = 5000
sys.setrecursionlimit(iMaxStackSize)

twitch = Twitch('msopj3elolkfedu4zxkamqb5koywm3', 'mr36ie37di0w5tjrhah4lma0nh7aq8')
twitch.authenticate_app([])

database = 'Overwatch.db'
conn = sqlite3.connect(database)
curr = conn.cursor()
n_select = 30
curr.execute('SELECT * FROM user_db ORDER BY FOLLOWERS DESC LIMIT {}'.format(n_select))
# curr.execute('SELECT * FROM bilibili_db ORDER BY FOLLOWERS DESC LIMIT {} OFFSET 50'.format(n_select))
data = curr.fetchall()
Pineline = EdgesPipeline()

for row in tqdm(data):
    id = str(row[0])
    print(id)
    cursor = []
    cursee = []

    Pineline.follower_parse(id, cursor)
    Pineline.followee_parse(id, cursee)
