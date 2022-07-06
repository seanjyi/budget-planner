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
  global page_size, type_income
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
        type_income = pd.read_sql_query('SELECT * FROM type_expense', connection)
      # checks type of loan
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='type_loan')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE type_loan (
        type TEXT NOT NULL
        )''')
      else:
        type_income = pd.read_sql_query('SELECT * FROM type_loan', connection)
      # checks type of pay
      if c.execute("SELECT EXISTS (SELECT name FROM sqlite_master WHERE type='table' AND name='type_pay')").fetchone()[0] == 0:
        c.execute('''CREATE TABLE type_pay (
        type TEXT NOT NULL
        )''')
      else:
        type_income = pd.read_sql_query('SELECT * FROM type_pay', connection)

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

'''Helper function for sorting'''
def sortByValue(list):
  return list['type']

'''
Sets initial page size to 10.
If defualt value is saved, loads that value.
'''
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

'''
Loads previous dropdown income values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-inc-tbl', 'data'),
  Input('sett-inc-button', 'n_clicks'),
  State('sett-inc-tbl', 'data'),
  State('sett-inc-input', 'value')
)
def sett_inc_add(n_clicks, data, value):
  global type_income
  if data == None:
    return type_income.to_dict('records')
  elif value == None or value == '':
    return no_update
  else: 
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_income', con=connection, if_exists='replace', index=False)

    type_income = pd.DataFrame(data=data)
    return data

'''
Loads previous dropdown expense values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-exp-tbl', 'data'),
  Input('sett-exp-button', 'n_clicks'),
  State('sett-exp-tbl', 'data'),
  State('sett-exp-input', 'value')
)
def sett_exp_add(n_clicks, data, value):
  global type_expense
  if data == None:
    return type_expense.to_dict('records')
  elif value == None or value == '':
    return no_update
  else: 
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_expense', con=connection, if_exists='replace', index=False)

    type_expense = pd.DataFrame(data=data)
    return data


'''
Loads previous dropdown loan values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-loan-tbl', 'data'),
  Input('sett-loan-button', 'n_clicks'),
  State('sett-loan-tbl', 'data'),
  State('sett-loan-input', 'value')
)
def sett_loan_add(n_clicks, data, value):
  global type_loan
  if data == None:
    return type_loan.to_dict('records')
  elif value == None or value == '':
    return no_update
  else: 
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_loan', con=connection, if_exists='replace', index=False)

    type_loan = pd.DataFrame(data=data)
    return data


'''
Loads previous dropdown payment values.
Adds new values, when button is clicked.
Ignores null or empty values.
'''
@callback(
  Output('sett-pay-tbl', 'data'),
  Input('sett-pay-button', 'n_clicks'),
  State('sett-pay-tbl', 'data'),
  State('sett-pay-input', 'value')
)
def sett_pay_add(n_clicks, data, value):
  global type_pay
  if data == None:
    return type_pay.to_dict('records')
  elif value == None or value == '':
    return no_update
  else: 
    print(value)
    data.append({'type': value})
    data.sort(key=sortByValue)
    with closing(sqlite3.connect(DBLOC)) as connection:
      pd.DataFrame(data).to_sql('type_pay', con=connection, if_exists='replace', index=False)

    type_pay = pd.DataFrame(data=data)
    return data
  