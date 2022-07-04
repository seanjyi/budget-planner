'''
Handles dropdown and page sizes. Additionally,
can delete and export data into csv files.
'''

import sqlite3
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, no_update
from contextlib import closing
from base64 import b64decode
from io import StringIO
from layouts import INCOME_SAVE, CONFIRM_COL

'''Global variable to check previous data'''
page_size = 10

DBLOC = ':memory:' # change to 'data/budget.db' or ':memory:'

'''Initial load, checks for past data'''
def sett_init():
  global page_size
  with closing(sqlite3.connect(DBLOC)) as connection:
    with closing(connection.cursor()) as c:
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='page_size')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE page_size (
        size INTEGER NOT NULL
        )''')
        pd.DataFrame(data={'size': [page_size]}).to_sql('page_size', con=connection, if_exists='replace', index=False)
      else:
        page_size = pd.read_sql_query('SELECT * FROM page_size', connection)['size'].iloc[0]

def get_size():
  return page_size

def sortByValue(e):
  return e['']

@callback(
  Output('sett-size', 'value'),
  Input('sett-size', 'value')
)
def default_size(value):
  global page_size
  if ctx.triggered_id == None:
    return page_size
  else:
    page_size = value
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data={'size': [page_size]}).to_sql('page_size', con=connection, if_exists='replace', index=False)
    return value

@callback(
  Output('sett-inc-tbl', 'data'),
  Input('sett-inc-button', 'n_clicks'),
  State('sett-inc-tbl', 'data'),
  State('sett-inc-input', 'value'),
  prevent_initial_call=True
)
def sett_inc_add(n_clicks, data, value):
  if data == None:
    return [{'': value}]
  else: 
    data.append({'': value})
    data.sort(key=sortByValue)
    return data