import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "create table if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

items_table = "create table if not exists items (name text, price real)"
cursor.execute(items_table)

cursor.execute("insert into items values ('item1', 10.99)")

connection.commit()

connection.close()
