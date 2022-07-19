'''
Handles user input related to income. When there isn't
previous data, shows an option to add a CSV file or start
new data. Will show an editable data table when there is data.
Can change page size, save or add an additional row.
'''

from dash import Input, Output, State, callback, no_update
from time import sleep
import settings
import transactions
from layouts import INCOME_SAVE

trans_type = 'income'

'''Initial load, checks if there is new data'''
def income_init():
  transactions.init(trans_type)

# INCOME_NEW CALLBACKS

'''New income page.'''
@callback(
  Output('income-upload-error', 'hidden'),
  Output('income-trigger', 'data'),
  Input('income-upload', 'contents'),
  Input('income-empty', 'n_clicks'),
)
def new_income(upload, empty):
  return transactions.new(upload, empty, trans_type)

''' Page connection logic '''
@callback(
  Output('income-content', 'children'),
  Input('income-trigger', 'data'),
  prevent_initial_call=True
)
def income_connect(data):
  return transactions.connect(data, trans_type)

# INCOME_DATA CALLBACKS

'''Adds additional row'''
@callback(
  Output('income-tbl', 'data'),
  Input('income-add', 'n_clicks'),
  State('income-trigger', 'data'),
  State('income-tbl-data', 'data'),
  State('income-tbl', 'columns')
)
def income_add(add, initial, data, col):
  return transactions.add_row(add, initial, data, col, trans_type)

'''Updates income page size.'''
@callback(
  Output('income-tbl', 'page_size'),
  Output('income-size', 'value'),
  Input('income-page', 'n_clicks'),
  State('income-size', 'value'),
  State('sett-size-store', 'data')
)
def income_update_page(n_clicks, value, store):
  return transactions.update_page_size(n_clicks, value, store)

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
def income_dropdown(dropdown, inc, exp, loan, pay):
  if not settings.get_type_income().empty and not settings.get_type_pay().empty:
    return True, {
      'category': {
        'options': ([{'label': i, 'value': i} for i in settings.get_type_income()['type']]) if settings.get_type_loan().empty
        else ([{'label': i, 'value': i} for i in settings.get_type_income()['type']] + [{'label': i, 'value': i} for i in settings.get_type_loan()['type']])
      },
      'mop': {
        'options': [{'label': i, 'value': i} for i in settings.get_type_pay()['type']]
      },
      'repay': {
        'options': ([]) if settings.get_type_expense().empty
        else ([{'label': i, 'value': i} for i in settings.get_type_expense()['type']])
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

'''Keeps track of table data'''
@callback(
  Output('income-tbl-data', 'data'),
  Input('income-tbl', 'data')
)
def income_data(data):
  return data

'''Save file.'''
@callback(
  Output('income-save', 'children'),
  Output('income-save', 'style'),
  Output('income-button', 'key'),
  Input('income-save', 'n_clicks'),
  State('income-tbl', 'data'),
  prevent_initial_call=True
)
def income_save(n_clicks, data):
  return transactions.save_file(n_clicks, data, trans_type)  

'''
Loading time for save button. Visual 
to show that save completed.
'''
@callback(
  Output('income-button', 'children'),
  Input('income-button', 'key'),
  prevent_initial_call=True
)
def income_save_load(key):
  sleep(settings.SLEEP_TIME)
  return INCOME_SAVE
