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
type_income = pd.DataFrame()
type_expense = pd.DataFrame()
type_loan = pd.DataFrame()
type_pay = pd.DataFrame()

DBLOC = ':memory:' # change to 'data/budget.db' or ':memory:'

'''Initial load, checks for past data'''
def sett_init():
  global page_size, type_income, type_expense, type_loan, type_pay
  with closing(sqlite3.connect(DBLOC)) as connection:
    with closing(connection.cursor()) as c:
      # checks page size
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='page_size')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE page_size (
        size INTEGER NOT NULL
        )''')
        pd.DataFrame(data={'size': [page_size]}).to_sql('page_size', con=connection, if_exists='replace', index=False)
      else:
        page_size = pd.read_sql_query('SELECT * FROM page_size', connection)['size'].iloc[0]
      # checks type of income
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='type_income')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE type_income (
        type TEXT NOT NULL
        )''')
      else:
        type_income = pd.read_sql_query('SELECT * FROM type_income', connection)
      # checks type of expense
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='type_expense')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE type_expense (
        type TEXT NOT NULL
        )''')
      else:
        type_expense = pd.read_sql_query('SELECT * FROM type_expense', connection)
      # checks type of loan
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='type_loan')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE type_loan (
        type TEXT NOT NULL
        )''')
      else:
        type_loan = pd.read_sql_query('SELECT * FROM type_loan', connection)
      # checks type of pay
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='type_pay')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE type_pay (
        type TEXT NOT NULL
        )''')
      else:
        type_pay = pd.read_sql_query('SELECT * FROM type_pay', connection)
  print('settings page initialized')

'''Helper function for sorting'''
def sortByValue(list):
  return list['type']

'''Returns page size'''
def get_size():
  return page_size

'''Returns type of income'''
def get_type_income():
  return type_income

'''Returns type of expense'''
def get_type_expense():
  return type_expense

'''Returns type of loans'''
def get_type_loan():
  return type_loan

'''Returns type of payment'''
def get_type_pay():
  return type_pay

'''
Sets initial page size to 10.
If default value is saved, loads that value.
'''
@callback(
  Output('sett-size', 'value'),
  Output('sett-size-store', 'data'),
  Input('sett-size', 'value'),
  State('sett-size-store', 'data')
)
def default_size(value, store):
  if value == None and store == None:
    return page_size, page_size
  elif value == None:
    return store, store
  else:
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data={'size': [value]}).to_sql('page_size', con=connection, if_exists='replace', index=False)
    return value, value

'''
Loads previous dropdown income values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-inc-input', 'value'),
  Output('sett-inc-tbl', 'data'),
  Output('sett-inc-store', 'data'),
  Input('sett-inc-button', 'n_clicks'),
  Input('sett-inc-tbl', 'data'),
  State('sett-inc-input', 'value'),
  State('sett-inc-store', 'data')
)
def sett_inc_add(n_clicks, data, value, store):
  if data == None and store == None:
    return None, type_income.to_dict('records'), type_income.to_dict('records')
  elif data == None:
    return None, store, store
  elif ctx.triggered_id == 'sett-inc-tbl':
    return None, data, data
  elif value == None or value == '':
    return no_update, no_update, no_update
  else: 
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_income', con=connection, if_exists='replace', index=False)

    return None, data, data

'''
Loads previous dropdown expense values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-exp-input', 'value'),
  Output('sett-exp-tbl', 'data'),
  Output('sett-exp-store', 'data'),
  Input('sett-exp-button', 'n_clicks'),
  Input('sett-exp-tbl', 'data'),
  State('sett-exp-input', 'value'),
  State('sett-exp-store', 'data')
)
def sett_exp_add(n_clicks, data, value, store):
  if data == None and store == None:
    return None, type_expense.to_dict('records'), type_expense.to_dict('records')
  elif data == None:
    return None, store, store
  elif ctx.triggered_id == 'sett-exp-tbl':
    return None, data, data
  elif value == None or value == '':
    return no_update, no_update, no_update
  else: 
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_expense', con=connection, if_exists='replace', index=False)

    return None, data, data

'''
Loads previous dropdown loan values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-loan-input', 'value'),
  Output('sett-loan-tbl', 'data'),
  Output('sett-loan-store', 'data'),
  Input('sett-loan-button', 'n_clicks'),
  Input('sett-loan-tbl', 'data'),
  State('sett-loan-input', 'value'),
  State('sett-loan-store', 'data')
)
def sett_loan_add(n_clicks, data, value, store):
  if data == None and store == None:
    return None, type_loan.to_dict('records'), type_loan.to_dict('records')
  elif data == None:
    return None, store, store
  elif ctx.triggered_id == 'sett-loan-tbl':
    return None, data, data
  elif value == None or value == '':
    return no_update, no_update, no_update
  else: 
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_loan', con=connection, if_exists='replace', index=False)

    return None, data, data

'''
Loads previous dropdown payment values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-pay-input', 'value'),
  Output('sett-pay-tbl', 'data'),
  Output('sett-pay-store', 'data'),
  Input('sett-pay-button', 'n_clicks'),
  Input('sett-pay-tbl', 'data'),
  State('sett-pay-input', 'value'),
  State('sett-pay-store', 'data')
)
def sett_pay_add(n_clicks, data, value, store):
  if data == None and store == None:
    return None, type_pay.to_dict('records'), type_pay.to_dict('records')
  elif data == None:
    return None, store, store
  elif ctx.triggered_id == 'sett-pay-tbl':
    return None, data, data
  elif value == None or value == '':
    return no_update, no_update, no_update
  else: 
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_pay', con=connection, if_exists='replace', index=False)

    return None, data, data
  