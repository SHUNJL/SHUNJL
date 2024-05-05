import sqlite3 as sql
conn = sql.connect('date_cloud.sql')

cursor = conn.cursor()
conn.commit