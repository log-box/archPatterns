import sqlite3

connect = sqlite3.connect('framework_board.sqlite')
cursor = connect.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cursor.executescript(text)
cursor.close()
connect.close()