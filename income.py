'''
Handles user input related to income. When there isn't
previous data, shows an option to add a CSV file or start
new data. Will show an editable data table when there is data.
Can change page size, save or add an additional row.
'''

import sqlite3
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, no_update
from contextlib import closing
from base64 import b64decode
from io import StringIO
from time import sleep
from settings import DBLOC, get_size
from layouts import INCOME_SAVE, CONFIRM_COL

'''Global variable to show different sections'''
income_df = pd.DataFrame(data=range(5))
show_new = True  # true to show income_new
first_read = True # true when initializing reading
tbl_exists = False # true when there is inital data 
page_first = True

'''Initial load, checks if there is new data'''
def income_init():
  global show_new, income_df, tbl_exists
  with closing(sqlite3.connect(DBLOC)) as connection:
    with closing(connection.cursor()) as c:
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='income')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE income (
        date INTEGER NOT NULL,
        category NOT NULL,
        amount MONEY NOT NULL,
        mop NOT NULL,
        notes
        )''')
      else:
        income_df = pd.read_sql_query('SELECT * FROM income', connection)
        show_new = False
        tbl_exists = True

''' Income table update logic '''
@callback(
  Output('income-new', 'hidden'),
  Output('income-data', 'hidden'),
  Output('income-tbl', 'data'),
  Output('income-error', 'hidden'),
  Input('income-upload', 'contents'),
  Input('income-empty', 'n_clicks'),
  Input('income-add', 'n_clicks'),
  State('income-tbl-data', 'data'),
  State('income-tbl', 'columns')
)
def data_update(upload, empty, add, data, col):
  global tbl_exists, first_read
  trigger_id = ctx.triggered_id
  if trigger_id == 'income-upload' and upload is not None:
    return load_data(upload)
  elif trigger_id == 'income-empty' and empty > 0:
    return init_data()
  elif trigger_id == 'income-add' and add > 0:
    return add_row(data, col)
  elif tbl_exists and first_read:
    first_read = False
    return not show_new, show_new, income_df.to_dict('records'), no_update
  else:
    return not show_new, show_new, data, no_update

'''Keeps track of table data'''
@callback(
  Output('income-tbl-data', 'data'),
  Input('income-tbl', 'data')
)
def data_tracker(data):
  return data

# INCOME_NEW CALLBACKS

'''Selected file to load'''
def load_data(upload):
  try:
    upload_type, upload_string = upload.split(',')
    if upload_type != 'data:application/vnd.ms-excel;base64':
      raise Exception()

    global show_new
    show_new = False
    df = pd.read_csv(StringIO(b64decode(upload_string).decode('utf-8')))
    return not show_new, show_new, df.to_dict('records'), no_update
  except Exception:
    return no_update, no_update, no_update, False

'''Selected new data'''
def init_data():
  global show_new
  show_new = False
  return not show_new, show_new, income_df.to_dict('records'), no_update

# INCOME_DATA CALLBACKS

'''
Updates page size. When initally loading the app,
will take default page size from sql.
If reloading, will take from dcc.Store.
If by button, will take from value.
'''
@callback(
  Output('income-tbl', 'page_size'),
  Output('income-size', 'value'),
  Output('income-page-size', 'data'),
  Input('income-page', 'n_clicks'),
  State('income-size', 'value'),
  State('income-page-size', 'data')
)
def update_page_size(n_clicks, value, data):
  global page_first
  if n_clicks == 0 and page_first:
    page_first = False
    return get_size(), get_size(), get_size()
  elif n_clicks == 0 and not page_first:
    return data, data, data
  else:
    return value, value, value

'''
Adds additional row when clicked.
Also, when initally loaded, corrects date formatting
and sorts by date.
'''
def add_row(data, columns):
  data.append({c['id']: '' for c in columns})
  return no_update, no_update, data, no_update

'''
Save file. If file exists, creates backups
Additionally, updates the dataframe when saved.
'''
@callback(
  Output('income-save', 'children'),
  Output('income-save', 'style'),
  Output('income-button', 'key'),
  Input('income-save', 'n_clicks'),
  State('income-tbl', 'data'),
  prevent_initial_call=True
)
def save_file(n_clicks, data):
  with closing(sqlite3.connect(DBLOC)) as connection:
    pd.DataFrame(data).to_sql('income', con=connection, if_exists='replace', index=False)
    # print(pd.read_sql_query('SELECT * FROM income', connection))
  return 'Saved!', {'borderRadius': '25px', 'width':'125px', 'background-color': CONFIRM_COL}, 'load_trigger'

'''
Loading time for save button. Visual 
to show that save completed.
'''
@callback(
  Output('income-button', 'children'),
  Input('income-button', 'key'),
  prevent_initial_call=True
)
def save_load(key):
  sleep(2)
  return INCOME_SAVE
