'''
Contains all the layouts of the application.
Layouts are all stored here to make individual page code 
easy to read.
'''
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme, Symbol

# HOME PAGE 

'''home page layout'''
home_layout = html.Div([
  html.H1('HOME: UNDER CONSTRUCTION')
])

# INCOME PAGE

'''no income database table layout'''
income_new = html.Div([
  html.Div('Selected file type must be CSV', id='income-error', hidden=True, style={'color': '#D62828'}),
  dcc.Upload(
    id='income-upload',
    children=html.Div(['Drag and Drop or Select CSV']),
    style={
      'width': '400px', 'height': '60px', 'lineHeight': '60px',
      'borderWidth': '1px', 'borderStyle': 'dashed',
      'borderRadius': '25px', 'textAlign': 'center'
    }
  ),
  html.Plaintext(
    "or"
  ),
  dbc.Button(
    id='income-empty',
    children='New Data',
    n_clicks=0,
    color='info',
    style={
      'borderRadius': '25px'
    }
  )
],
# positions upload and new data button to middle of screen
style={
  'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
  'position': 'absolute', 'top': '50%', 'left': '50%',
  'transform': 'translate(-50%, -50%)'
},
hidden=True,
id='income-new'
)

input_group = dbc.InputGroup(
  [
    dbc.Input(id='income-size', type='number'),
    dbc.Button(id='income-page', n_clicks=0, children='Page Size'),
  ],
  size='sm',
  style={'width': '180px'}
)

'''income database table layout'''
income_data = html.Div([
  # title and page size control
  dbc.Row(
    [
      dbc.Col(html.H1('Income', style={'text-align': 'center'})),
      dbc.Col(),
      dbc.Col(input_group, align='end', width='auto'),    
    ]
  ),
  dash_table.DataTable(
    id='income-tbl',
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
  # positions add and save button
  dbc.Row(
    [
      dbc.Col(dbc.Button(id='income-add', n_clicks=0, children='Add Row', color='primary'), width='auto'),
      dbc.Col(dbc.Button(id='income-save', n_clicks=0, children='Save', color='info'), width='auto'),
    ],
    justify='evenly'
  ),
  dbc.Row(dbc.Alert(id='income-saved', children='✓: Data Saved', color='#2FDD92', fade=False, is_open=False, duration=1000,
    style={'color': 'white', 'text-align': 'center', 'line-height': '4px'}),
    style={'width': '250px', 'margin-left': 'auto', 'margin-right': 'auto'}
  )],
  hidden=True,
  id='income-data'
) 

'''income page layout'''
income_layout = html.Div([income_new, income_data])

# EXPENSE PAGE

expense_layout = html.Div([
    html.H3('Warning: Construction Zone')
])

# SETTINGS PAGE

settings_layout = html.Div([
    html.H3('Warning: Construction Zone')
])