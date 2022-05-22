from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from os.path import exists
from os import rename, remove

try:
  df = pd.read_csv('data/income.csv')
except OSError as e:
  df = pd.DataFrame(index=range(1), columns=range(5))

input_group = dbc.InputGroup(
  [
    dbc.Input(id='size-input', type='number'),
    dbc.Button(id='page-button', n_clicks=0, children='Page Size'),
  ],
  size='sm',
  style={'width': '180px'}
)

layout = html.Div([
  dbc.Row(
    [
      dbc.Col(html.H1('Income', style={'text-align': 'center'})),
      dbc.Col(),
      dbc.Col(input_group, align='end', width='auto'),    
    ]
  ),
  dash_table.DataTable(
    id='tbl',
    style_data={
      'whiteSpace': 'normal',
      'height': 'auto',
      'lineHeight': '15px'
    },
    data=df.to_dict('records'),
    columns=[{
      'id': 'date', 'name': 'Date', 'type': 'datetime'
    }, {
      'id': 'category', 'name': 'Category', 'type': 'text'
    }, {
      'id': 'amount', 'name': 'Amount ($)', 'type': 'numeric'
    }, {
      'id': 'mop', 'name': 'MOP', 'type': 'text'
    }, {
      'id': 'notes', 'name': 'Notes', 'type': 'text'
    }],
    editable=True,
    row_deletable=True
  ),
  dbc.Row(
    [
      dbc.Col(dbc.Button(id='add-button', n_clicks=0, children='Add Row', color='primary'), width='auto'),
      dbc.Col(dbc.Button(id='save-button', n_clicks=0, children='Save', color='info'), width='auto'),
    ],
    justify='evenly'
  )
]) 

# when page size button is clicked updates # of rows per page
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

# when add row button is clicked, add a row
@callback(
  Output('tbl', 'data'),
  Input('add-button', 'n_clicks'),
  State('tbl', 'data'),
  State('tbl', 'columns')
)
def add_row(n_clicks, rows, columns):
  if n_clicks > 0:
    rows.append({c['id']: '' for c in columns})
  return rows

# saves file, when pressed
@callback(
  Output('save-button', 'n_clicks'),
  Input('save-button', 'n_clicks')
)
def save_file(n_clicks):
  if n_clicks > 0:
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
    df.to_csv('data/income.csv', index=False)
  return n_clicks
