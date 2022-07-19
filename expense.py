'''
Handles user input related to expense. When there isn't
previous data, shows an option to add a CSV file or start
new data. Will show an editable data table when there is data.
Can change page size, save or add an additional row.
'''

from dash import Input, Output, State, callback, no_update
from time import sleep
import settings
import transactions
from layouts import EXPENSE_SAVE

trans_type = 'expense'

'''Initial load, checks if there is new data'''
def expense_init():
  transactions.init(trans_type)

# EXPENSE_NEW CALLBACKS

'''New expense page.'''
@callback(
  Output('expense-upload-error', 'hidden'),
  Output('expense-trigger', 'data'),
  Input('expense-upload', 'contents'),
  Input('expense-empty', 'n_clicks'),
)
def new_expense(upload, empty):
  return transactions.new(upload, empty, trans_type)

''' Page connection logic '''
@callback(
  Output('expense-content', 'children'),
  Input('expense-trigger', 'data'),
  prevent_initial_call=True
)
def expense_connect(data):
  return transactions.connect(data, trans_type)

# EXPENSE_DATA CALLBACKS

'''Adds additional row'''
@callback(
  Output('expense-tbl', 'data'),
  Input('expense-add', 'n_clicks'),
  State('expense-trigger', 'data'),
  State('expense-tbl-data', 'data'),
  State('expense-tbl', 'columns')
)
def expense_add(add, initial, data, col):
  return transactions.add_row(add, initial, data, col, trans_type)

'''Updates expense page size.'''
@callback(
  Output('expense-tbl', 'page_size'),
  Output('expense-size', 'value'),
  Input('expense-page', 'n_clicks'),
  State('expense-size', 'value'),
  State('sett-size-store', 'data')
)
def expense_update_page(n_clicks, value, store):
  return transactions.update_page_size(n_clicks, value, store)

'''
Updates dropdown.
'''
@callback(
  Output('expense-tbl-error', 'hidden'),
  Output('expense-tbl', 'dropdown'),
  Input('expense-tbl', 'dropdown'),
  State('sett-exp-store', 'data'),
  State('sett-loan-store', 'data'),
  State('sett-pay-store', 'data')
)
def expense_dropdown(dropdown, exp, loan, pay):
  if not settings.get_type_expense().empty and not settings.get_type_pay().empty:
    return True, {
      'mop': {
        'options': [{'label': i, 'value': i} for i in settings.get_type_pay()['type']]
      },
      'category': {
        'options': ([{'label': i, 'value': i} for i in settings.get_type_expense()['type']]) if settings.get_type_loan().empty
        else ([{'label': i, 'value': i} for i in settings.get_type_expense()['type']] + [{'label': i, 'value': i} for i in settings.get_type_loan()['type']])
      }
    }
  elif exp and pay:
    return True, {
      'mop': {
        'options': [{'label': i.get('type'), 'value': i.get('type')} for i in pay]
      },
      'category': {
        'options': ([{'label': i.get('type'), 'value': i.get('type')} for i in exp]) if loan == None
        else ([{'label': i.get('type'), 'value': i.get('type')} for i in exp] + [{'label': i.get('type'), 'value': i.get('type')} for i in loan])
      }
    }
  else:
    return False, no_update

'''Keeps track of table data'''
@callback(
  Output('expense-tbl-data', 'data'),
  Input('expense-tbl', 'data')
)
def expense_data(data):
  return data

'''Save file.'''
@callback(
  Output('expense-save', 'children'),
  Output('expense-save', 'style'),
  Output('expense-button', 'key'),
  Input('expense-save', 'n_clicks'),
  State('expense-tbl', 'data'),
  prevent_initial_call=True
)
def expense_save(n_clicks, data):
  return transactions.save_file(n_clicks, data, trans_type)  

'''
Loading time for save button. Visual 
to show that save completed.
'''
@callback(
  Output('expense-button', 'children'),
  Input('expense-button', 'key'),
  prevent_initial_call=True
)
def expense_save_load(key):
  sleep(settings.SLEEP_TIME)
  return EXPENSE_SAVE