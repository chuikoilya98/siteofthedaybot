import datetime
import sqlite3
import os.path as pt

conn = sqlite3.connect(pt.abspath('database.db'))

cursor = conn.cursor()
conn.execute("""CREATE TABLE users (id text, name text)""")
conn.execute("""CREATE TABLE sites (id text, url text, added_by text, tags text)""")
