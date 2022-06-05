# import required module
import sqlite3
import pandas as pd

# connect to database
conn = sqlite3.connect(':memory:')
 
# create cursor object
cur = conn.cursor()

with conn:
  # create tables
  cur.execute("""CREATE TABLE income (
    date INTEGER NOT NULL,
    category NOT NULL,
    amount MONEY NOT NULL,
    mop NOT NULL,
    notes
  );""")
  print('inocme table created')
 
  # # check if table exists
  # print('Check if INCOME table exists in the database:')
  # listOfTables = cur.execute(
  #   """SELECT name FROM sqlite_master WHERE type='table' AND name='INCOME'; """).fetchall()
  
  # print(listOfTables)
  cur.execute("""CREATE TABLE income (
    date INTEGER NOT NULL,
    category NOT NULL,
    amount MONEY NOT NULL,
    mop NOT NULL,
    notes
  );""")
  cur.execute('''INSERT INTO income VALUES ( 'h', 'fjdsklf', 'sdfs', 'sdfsdf', NULL)''')
  cur.execute('''SELECT * FROM income ''')
  print(cur.fetchall())

  info = cur.execute("PRAGMA table_info('income')").fetchall()
  columns = [item[0] for item in cur.description]

  df = pd.DataFrame(info, columns=columns)

  print(df)

# terminate the connection
conn.close()