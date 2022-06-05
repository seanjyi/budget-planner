'''
Handles user input related to income. Shows a data table
that the user can edit or add to. Additionally, can save the 
data table or change page size.
'''

from dash import Input, Output, State, callback, ctx, no_update
import pandas as pd
from os.path import exists
from os import rename, remove
from settings import connection
from contextlib import closing
from base64 import b64decode
from io import StringIO

'''Global variable to show different pages'''
show_new = True # true to show income_new

'''Initial load, checks if there is new data'''
with closing(connection.cursor()) as c:
  if c.execute('''SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='income')''').fetchone()[0] == 0:
    c.execute("""CREATE TABLE income (
      date INTEGER NOT NULL,
      category NOT NULL,
      amount MONEY NOT NULL,
      mop NOT NULL,
      notes
    );""")
    connection.commit()
    show_new=True
  else:
    show_new=False
    # load table info

# income table update logic
@callback(
  Output('income-new', 'hidden'),
  Output('income-data', 'hidden'),
  Output('income-tbl', 'data'),
  Output('income-error', 'is_open'),
  Input('income-upload', 'contents'),
  Input('income-empty', 'n_clicks'),
  Input('income-add', 'n_clicks'),
  State('income-tbl-data', 'data'),
  State('income-tbl', 'columns')
)
def data_update(upload, empty, add, data, col):
  trigger_id = ctx.triggered_id
  if trigger_id == 'income-upload' and upload is not None:
    return load_data(upload)
  elif trigger_id == 'income-empty' and empty != 0:
    return init_data()
  elif trigger_id == 'income-add' and add != 0:
    return add_row(data, col)
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
    show_new=False
    df = pd.read_csv(StringIO(b64decode(upload_string).decode('utf-8')))
    return not show_new, show_new, df.to_dict('records'), no_update
  except Exception as e:
    return no_update, no_update, no_update, True

'''Selected new data'''
def init_data():
  global show_new
  show_new=False
  return not show_new, show_new, pd.DataFrame(data=range(5)).to_dict('records'), no_update

# INCOME_DATA CALLBACKS

'''Updates page size'''
@callback(
  Output('income-tbl', 'page_size'),
  Output('page-size', 'data'),
  Output('income-size', 'value'),
  Input('income-page', 'n_clicks'),
  State('income-size', 'value'),
  State('page-size', 'data')    
)
def update_page_size(n_clicks, value, data):
  if n_clicks == 0:
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
  Output('income-save', 'n_clicks'),
  Input('income-save', 'n_clicks'),
  State('income-tbl', 'data')
)
def save_file(n_clicks, data):
  if n_clicks > 0:
    global income_df
    income_df = pd.DataFrame(data)

    if exists('data/income.csv'):
      i = 1
      while(i < 6 and exists('data/income-backup-{}.csv'.format(i))):
        i+= 1
      for j in range(i,1,-1):
        if j == 6:
          remove('data/income-backup-{}.csv'.format(j-1))
        else:
          rename('data/income-backup-{}.csv'.format(j-1), 'data/income-backup-{}.csv'.format(j))
      rename('data/income.csv', 'data/income-backup-1.csv')
    income_df.to_csv('data/income.csv', index=False)
  return n_clicks
