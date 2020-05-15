import sqlite3

conn = sqlite3.connect('bilibili_music_original_01032020_31032020.db')
c = conn.cursor()

c.execute('SELECT * FROM bilibili_db')
data = c.fetchall()
print(data)