'''
Contains all the layouts of the application.
Layouts are all stored here to make individual page code 
easy to read.
'''
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme, Symbol

# Order of parameters: id > children > style > etc

INCOME_SAVE = dbc.Button(id='income-save', n_clicks=0, children='Save', color='info', style={'borderRadius': '25px', 'width':'100px'})

MAIN_COL = 'LightSlateGrey'
ERROR_COL = '#D62828'
CONFIRM_COL = '#2FDD92'
PERSISTENCE_TYPE = 'memory' # later change to session, so browser can remember

INIT_PAGE_SIZE = 10

# HOME PAGE 

'''home page layout'''
home_layout = html.Div([html.H1('HOME: UNDER CONSTRUCTION')])

# INCOME PAGE

'''no income database table layout'''
income_new = html.Div(
  id='income-new',
  children=[
    html.Div(
      id='income-error', 
      children='Selected file type must be CSV',
      style={'color': ERROR_COL},
      hidden=True
    ),
    dcc.Upload(
      id='income-upload',
      children=html.Div(['Drag and Drop or Select CSV']),
      style={
        'width': '400px', 'height': '60px', 'lineHeight': '60px',
        'borderWidth': '1px', 'borderStyle': 'dashed',
        'borderRadius': '50px', 'textAlign': 'center'
      }
    ),
    html.Plaintext('or'),
    dbc.Button(
      id='income-empty',
      children='New Data',
      style={'borderRadius': '25px'},
      n_clicks=0,
      color='info'
    )
  ],
  # positions upload and new data button to middle of screen
  style={
    'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
    'position': 'absolute', 'top': '50%', 'left': '50%',
    'transform': 'translate(-50%, -50%)'
  },
  hidden=True
)

input_group = dbc.InputGroup(
  children=[
    dbc.Input(
      id='income-size', 
      style={'border-radius': '25px 0 0 25px'}, 
      value=INIT_PAGE_SIZE, 
      type='number', 
      min=1, 
      persistence=True, 
      persistence_type=PERSISTENCE_TYPE
    ),
    dbc.Button(
      id='income-page', 
      children='Page Size', 
      style={'border-radius': '0 25px 25px 0', 'background-color': MAIN_COL}, 
      n_clicks=0
    ),
  ],
  style={'width': '180px', 'margin-right': '10px', 'margin-bottom': '10px'},
  size='sm'
)

'''income database table layout'''
income_data = html.Div(
  id='income-data',
  children=[
    # title and page size control
    dbc.Row(
      children=[
        dbc.Col(html.H1('Income', style={'text-align': 'center'})),
        dbc.Col(),
        dbc.Col(input_group, align='end', width='auto'),    
      ],
      style={'margin-top': '10px'}
    ),
    dash_table.DataTable(
      id='income-tbl',
      columns=[
        {'id': 'date', 'name': 'Date', 'type': 'datetime'}, 
        {'id': 'category', 'name': 'Category', 'type': 'text'},
        {'id': 'amount', 'name': 'Amount ($)', 'type': 'numeric', 'format': Format(precision=2, symbol=Symbol.yes, scheme=Scheme.fixed).group(True)}, 
        {'id': 'mop', 'name': 'MOP', 'type': 'text'},
        {'id': 'notes', 'name': 'Notes', 'type': 'text'}
      ],
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
        dbc.Col(dbc.Button(id='income-add', n_clicks=0, children='Add Row', style={'borderRadius': '25px', 'background-color': MAIN_COL}), width='auto'),
        dbc.Col(id='income-button', children=INCOME_SAVE, width='auto'),
      ],
      style={'margin-top': '50px'},
      justify='evenly'
    ),
  ],
  hidden=True
) 

'''income page layout'''
income_layout = html.Div([income_new, income_data])

# EXPENSE PAGE

expense_layout = html.Div([html.H3('Warning: Construction Zone')])

# SETTINGS PAGE

def dropdown_template(title, input, button, table):
  return html.Div([
    html.H3(title, style={'margin-left': '50px'}),
    dbc.InputGroup(
    children=[ # settinc is settings + income
      dbc.Input(id=input, type='text'),
      dbc.Button(id=button, children='Add', style={'background-color': MAIN_COL}, n_clicks=0),
    ],
    style={'margin-left': '100px', 'width': '400px'},
    size='sm'
    ),
    dash_table.DataTable(
      id=table,
      row_deletable=True
    )
  ])

settings_layout = html.Div([
  html.H3('Default Page Size', style={'margin-left': '50px'}),
  dbc.Input(id='setting-size', style={'margin-left': '100px', 'width': '400px'}, type='number', min=1, size='sm'),
  dropdown_template('Type of Income', 'settinc', 'settinc-button', 'settinc-tbl'),
  dropdown_template('Type of Expense', 'settexp', 'settexp-button', 'settexp-tbl'),
  dropdown_template('Type of Loan', 'settloan', 'settloan-button', 'sett-tbl'),
  dropdown_template('Payment Method', 'settmop', 'settmop-button', 'settmop-tbl'),
  html.H3('Export Data', style={'margin-left': '50px', 'color': CONFIRM_COL}),
  html.H3('Delete Data', style={'margin-left': '50px', 'color': ERROR_COL}),
])