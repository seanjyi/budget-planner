'''
Handles user input related to income. Shows a data table
that the user can edit or add to. Additionally, can save the 
data table or change page size.
'''

from dash import html, Input, Output, State, callback, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from os.path import exists
from os import rename, remove
from dash.dash_table.Format import Format, Scheme, Symbol

'''Reads in data'''
try:
  income_df = pd.read_csv('data/income.csv')
except OSError as e:
  income_df = pd.DataFrame(data=range(5))

input_group = dbc.InputGroup(
  [
    dbc.Input(id='size-input', type='number'),
    dbc.Button(id='page-button', n_clicks=0, children='Page Size'),
  ],
  size='sm',
  style={'width': '180px'}
)

'''Income data table page layout'''
table_layout = html.Div([
  dbc.Row(
    [
      dbc.Col(html.H1('Income', style={'text-align': 'center'})),
      dbc.Col(),
      dbc.Col(input_group, align='end', width='auto'),    
    ]
  ),
  dash_table.DataTable(
    id='tbl',
    columns=[{
      'id': 'date', 'name': 'Date', 'type': 'datetime'
    }, {
      'id': 'category', 'name': 'Category', 'type': 'text'
    }, {
      'id': 'amount', 'name': 'Amount ($)', 'type': 'numeric', 'format': Format(precision=2, symbol=Symbol.yes, scheme=Scheme.fixed).group(True)
    }, {
      'id': 'mop', 'name': 'MOP', 'type': 'text'
    }, {
      'id': 'notes', 'name': 'Notes', 'type': 'text'
    }],
    style_cell={'text-align': 'center'},
    style_cell_conditional=[{
      'if': {'column_id': 'notes'}, 'text-align': 'left'
    }],
    style_data={
      'height': 'auto',
      'lineHeight': '15px'
    },
    style_data_conditional=[{
      'if': {'column_id': 'notes'}, 'whiteSpace': 'normal'
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

'''Income first user layout'''
new_layout = html.Div([
  dcc.Upload(
    id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select CSV')
        ]),
        style={
            'width': '400px', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '50px', 'textAlign': 'center'
        }
  ),
  html.Plaintext(
    "or"
  ),
  dbc.Button(
    id='income-new',
    children='New Data',
    n_clicks=0,
    color='info',
    style={
      'borderRadius': '50px'
    }
  )
],
style={
  'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
  'position': 'absolute', 'top': '50%', 'left': '50%',
  'transform': 'translate(-50%, -50%)'
})

layout = new_layout