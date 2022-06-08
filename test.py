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
  print(cur.fetchall())

# terminate the connection
conn.close()