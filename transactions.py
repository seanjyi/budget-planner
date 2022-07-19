'''
Parent file for income and expenses.
Holds methods that both commonly use.
'''

import sqlite3
import pandas as pd
from dash import ctx, no_update
from contextlib import closing
from base64 import b64decode
from io import StringIO
import settings
from layouts import CONFIRM_COL, income_data, expense_data

# INIT

'''Initial load, checks if there is new data'''
def init(transaction):
  with closing(sqlite3.connect(settings.DBLOC)) as connection:
    with closing(connection.cursor()) as c:
      if c.execute(f"SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='{transaction}')").fetchone()[0] == 0:
        c.execute(f'''CREATE TABLE {transaction} (
        date INTEGER NOT NULL,
        category NOT NULL,
        amount MONEY NOT NULL,
        mop NOT NULL,
        notes
        )''')
      else:
        settings.set_transaction(pd.read_sql_query(f'SELECT * FROM {transaction}', connection), transaction)
  print(f'{transaction} page initialized')

# NEW PAGE LOGIC

'''
New page. If there is loaded data, load data.
Else, recieve from upload or start fresh.
'''
def new(upload, empty, transaction):
  trigger_id = ctx.triggered_id
  if not settings.get_transaction(transaction).empty:
    return no_update, 'load'
  elif trigger_id == f'{transaction}-upload' and upload is not None:
    upload_type, upload_string = upload.split(',')
    if upload_type != 'data:application/vnd.ms-excel;base64':
      return False, no_update
    else:
      return no_update, upload_string
  elif trigger_id == f'{transaction}-empty' and empty > 0:
    return no_update, 'empty'
  else:
    return no_update, no_update

'''Changes to data page'''
def connect(data, transaction):
  if data != None:
    if transaction == 'income':
      return [income_data]
    else:
      return [expense_data]
  else:
    return no_update

# DATA PAGE LOGIC

'''
Initializes given data
'''
def inititalize_data(initial, transaction):
  if initial == 'load':
    return settings.get_transaction(transaction).to_dict('records')    
  elif initial == 'empty':
    return pd.DataFrame(data=range(5)).to_dict('records')
  else:
    return pd.read_csv(StringIO(b64decode(initial).decode('utf-8'))).to_dict('records')

'''
Inititalizes data and adds a row.
'''
def add_row(add, initial, data, col, transaction):
  if add > 0:
    data.append({c['id']: '' for c in col})
    return data
  elif data != None:
    return data
  else:
    return inititalize_data(initial, transaction)

'''
Updates page size. When initally loading the app or page,
will take default page size from sql.
If by button, will take from value.
'''
def update_page_size(n_clicks, value, store):
  if n_clicks == 0 and store == None:
    return settings.get_size(), settings.get_size()
  elif n_clicks == 0:
    return store, store
  else:
    return value, value

'''
Save file. If file exists, creates backups
Additionally, updates the dataframe when saved.
'''
def save_file(n_clicks, data, transaction):
  with closing(sqlite3.connect(settings.DBLOC)) as connection:
    pd.DataFrame(data).to_sql(transaction, con=connection, if_exists='replace', index=False)
    # print(pd.read_sql_query('SELECT * FROM income', connection))
  return 'Saved!', {'borderRadius': '25px', 'width':'125px', 'background-color': CONFIRM_COL}, 'load_trigger'
