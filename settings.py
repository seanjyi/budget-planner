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
from time import sleep
from os.path import exists
from os import rename, remove
from layouts import INCOME_SAVE, CONFIRM_COL, ERROR_COL, INCOME_EXPORT, EXPENSE_EXPORT, INCOME_DELETE, EXPENSE_DELETE

'''Global variable to check previous data'''
page_size = 10
type_income = pd.DataFrame()
type_expense = pd.DataFrame()
type_loan = pd.DataFrame()
type_pay = pd.DataFrame()

DBLOC = 'data/budget.db' # change to 'data/budget.db' or ':memory:'

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

# EXPORT BUTTONS

'''
Save income dataset as a CSV file.
Creates backups if original exists.
'''
@callback(
  Output('export-income', 'children'),
  Output('export-income', 'style'),
  Output('export-inc-button', 'key'),
  Input('export-income', 'n_clicks'),
  State('income-tbl-data', 'data'),
  prevent_initial_call=True
)
def export_income(n_clicks, data):
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
  pd.DataFrame(data=data).to_csv('data/income.csv', index=False)
  return 'Saved!', {'borderRadius': '25px', 'width':'125px', 'background-color': CONFIRM_COL}, 'load_trigger'

'''
Loading time for income save button.
Visual to show save completed.
'''
@callback(
  Output('export-inc-button', 'children'),
  Input('export-inc-button', 'key'),
  prevent_initial_call=True
)
def export_income_load(key):
  sleep(2)
  return INCOME_EXPORT

'''
Save expense dataset as a CSV file.
Creates backups if original exists.
'''
@callback(
  Output('export-expense', 'children'),
  Output('export-expense', 'style'),
  Output('export-exp-button', 'key'),
  Input('export-expense', 'n_clicks'),
  State('income-tbl-data', 'data'), # CHANGE!!!!
  prevent_initial_call=True
)
def export_expense(n_clicks, data):
  return 'Saved!', {'borderRadius': '25px', 'width':'125px', 'background-color': CONFIRM_COL}, 'load_trigger'

'''
Loading time for expense save button.
Visual to show save completed.
'''
@callback(
  Output('export-exp-button', 'children'),
  Input('export-exp-button', 'key'),
  prevent_initial_call=True
)
def export_expense_load(key):
  sleep(2)
  return EXPENSE_EXPORT

# DELETE BUTTONS

'''
Delete income dataset.
Asks for a reconfirmation click  # possible to just delete from SQL and then it will give an empty frame.
'''
@callback(
  Output('delete-income', 'children'),
  Output('delete-income', 'style'),
  Output('delete-inc-button', 'key'),
  Output('income-trigger', 'clear_data'),
  Output('income-tbl-data', 'clear_data'),
  Input('delete-income', 'n_clicks'),
  prevent_initial_call=True
)
def delete_income(n_clicks):
  if n_clicks > 0:
    if n_clicks == 1:
      return 'Reclick', {'borderRadius': '25px', 'width':'125px', 'background-color': ERROR_COL}, no_update, no_update, no_update
    else:  
      with closing(sqlite3.connect(DBLOC)) as connection:
        with closing(connection.cursor()) as c:
          c.execute('DELETE from income')
          connection.commit()
          print('Deleted', c.rowcount, 'entries from income.')
      return 'Deleted!', {'borderRadius': '25px', 'width':'125px', 'background-color': ERROR_COL}, 'load_trigger', True, True
  else:
    return no_update, no_update, no_update, no_update, no_update

'''
Loading time for income delete button.
Visual to show delete completed.
'''
@callback(
  Output('delete-inc-button', 'children'),
  Input('delete-inc-button', 'key'),
  prevent_initial_call=True
)
def delete_income_load(key):
  sleep(2)
  return INCOME_DELETE

'''
Delete expense dataset.
Asks for a reconfirmation click
'''
@callback(
  Output('delete-expense', 'children'),
  Output('delete-expense', 'style'),
  Output('delete-exp-button', 'key'),
  Input('delete-expense', 'n_clicks'),
  State('delete-expense', 'children'),
  prevent_initial_call=True
)
def delete_expense(n_clicks, child):
  if child == 'Expense':
    return 'Reclick', {'borderRadius': '25px', 'width':'125px', 'background-color': ERROR_COL}, no_update
  else:
    return 'Deleted!', {'borderRadius': '25px', 'width':'125px', 'background-color': ERROR_COL}, 'load_trigger'

'''
Loading time for expense delete button.
Visual to show delete completed.
'''
@callback(
  Output('delete-exp-button', 'children'),
  Input('delete-exp-button', 'key'),
  prevent_initial_call=True
)
def delete_expense_load(key):
  sleep(2)
  return EXPENSE_DELETE
