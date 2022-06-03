'''
Handles user input related to income. Shows a data table
that the user can edit or add to. Additionally, can save the 
data table or change page size.
'''

from dash import Input, Output, State, callback
import pandas as pd
from os.path import exists
from os import rename, remove
from layouts import income_layout, new_layout

'''Reads in data'''
try:
  income_df = pd.read_csv('data/income.csv')
except OSError as e:
  income_df = pd.DataFrame(data=range(5))

layout = income_layout

'''Updates page size'''
@callback(
  Output('tbl', 'page_size'),
  Output('page-size', 'data'),
  Output('size-input', 'value'),
  Input('page-button', 'n_clicks'),
  State('size-input', 'value'),
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
@callback(
  Output('tbl', 'data'),
  Input('add-button', 'n_clicks'),
  State('tbl', 'data'),
  State('tbl', 'columns')
)
def add_row(n_clicks, data, columns):
  global income_df
  if n_clicks > 0:
    data.append({c['id']: '' for c in columns})
    return data
  elif 'date' in income_df:
    income_df['date'] = pd.to_datetime(income_df['date']).dt.date
    income_df = income_df.sort_values(by=['date'])
    return income_df.to_dict('records')
  else:
    return income_df.to_dict('records')

'''
Save file. If file exists, creates backups
Additionally, updates the dataframe when saved.
'''
@callback(
  Output('save-button', 'n_clicks'),
  Input('save-button', 'n_clicks'),
  State('tbl', 'data')
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
