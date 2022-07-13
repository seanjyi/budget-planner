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
from settings import DBLOC, get_size, get_type_income, get_type_expense, get_type_loan, get_type_pay
from layouts import INCOME_SAVE, CONFIRM_COL, income_data

'''Global variable to show different sections'''
income_df = pd.DataFrame()

'''Initial load, checks if there is new data'''
def income_init():
  global income_df
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
  print('income page initialized')

# INCOME_NEW CALLBACKS

''' 
New income page. If there is loaded data, load data.
Else, recieves data from upload or new data button.
'''
@callback(
  Output('income-upload-error', 'hidden'),
  Output('income-trigger', 'data'),
  Input('income-upload', 'contents'),
  Input('income-empty', 'n_clicks'),
)
def new_income(upload, empty):
  trigger_id = ctx.triggered_id
  if not income_df.empty:
    return no_update, 'load'
  elif trigger_id == 'income-upload' and upload is not None:
    upload_type, upload_string = upload.split(',')
    if upload_type != 'data:application/vnd.ms-excel;base64':
      return False, no_update
    else:
      return no_update, upload_string
  elif trigger_id == 'income-empty' and empty > 0:
    return no_update, 'empty'
  else:
    return no_update, no_update

''' Page connection logic '''
@callback(
  Output('income-content', 'children'),
  Input('income-trigger', 'data'),
  prevent_initial_call=True
)
def income_connect(data):
  if data != None:
    return [income_data]
  else:
    return no_update

# INCOME_DATA CALLBACKS

'''
Initializes given data
'''
def inititalize_data(initial):
  if initial == 'load':
    return income_df.to_dict('records')    
  elif initial == 'empty':
    return pd.DataFrame(data=range(5)).to_dict('records')
  else:
    return pd.read_csv(StringIO(b64decode(initial).decode('utf-8'))).to_dict('records')

'''
Updates page size. When initally loading the app or page,
will take default page size from sql.
If by button, will take from value.
'''
@callback(
  Output('income-tbl', 'page_size'),
  Output('income-size', 'value'),
  Input('income-page', 'n_clicks'),
  State('income-size', 'value'),
  State('sett-size-store', 'data')
)
def update_page_size(n_clicks, value, store):
  if n_clicks == 0 and store == None:
    return get_size(), get_size()
  elif n_clicks == 0:
    return store, store
  else:
    return value, value

'''
Updates dropdown.
Category dropdown is type of income with type of loans.
Payment dropdown is type of payments.
Repayment dropdown is type of expense.
Type of income and payment is necessary.
'''
@callback(
  Output('income-tbl-error', 'hidden'),
  Output('income-tbl', 'dropdown'),
  Input('income-tbl', 'dropdown'),
  State('sett-inc-store', 'data'),
  State('sett-exp-store', 'data'),
  State('sett-loan-store', 'data'),
  State('sett-pay-store', 'data')
)
def tbl_dropdown(dropdown, inc, exp, loan, pay):
  if not get_type_income().empty and not get_type_pay().empty:
    return True, {
      'category': {
        'options': ([{'label': i, 'value': i} for i in get_type_income()['type']]) if get_type_loan().empty
        else ([{'label': i, 'value': i} for i in get_type_income()['type']] + [{'label': i, 'value': i} for i in get_type_loan()['type']])
      },
      'mop': {
        'options': [{'label': i, 'value': i} for i in get_type_pay()['type']]
      },
      'repay': {
        'options': ([]) if get_type_expense().empty
        else ([{'label': i, 'value': i} for i in get_type_expense()['type']])
      }
    }
  elif inc and pay:
    return True, {
      'category': {
        'options': ([{'label': i.get('type'), 'value': i.get('type')} for i in inc]) if loan == None
        else ([{'label': i.get('type'), 'value': i.get('type')} for i in inc] + [{'label': i.get('type'), 'value': i.get('type')} for i in loan])
      },
      'mop': {
        'options': [{'label': i.get('type'), 'value': i.get('type')} for i in pay]
      },
      'repay': {
        'options': ([{'label': i.get('type'), 'value': i.get('type')} for i in exp])
      }
    }
  else:
    return False, no_update

'''
Adds additional row when clicked.
'''
@callback(
  Output('income-tbl', 'data'),
  Input('income-add', 'n_clicks'),
  State('income-trigger', 'data'),
  State('income-tbl-data', 'data'),
  State('income-tbl', 'columns')
)
def add_row(add, initial, data, col):
  if add > 0:
    data.append({c['id']: '' for c in col})
    return data
  elif data != None:
    return data
  else:
    return inititalize_data(initial)

'''Keeps track of table data'''
@callback(
  Output('income-tbl-data', 'data'),
  Input('income-tbl', 'data')
)
def data_tracker(data):
  return data

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
