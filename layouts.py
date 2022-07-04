'''
Contains all the layouts of the application.
Layouts are all stored here to make individual page code 
easy to read.
'''
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme, Symbol

# Order of parameters: id > children > style > etc

MAIN_COL = 'LightSlateGrey'
ERROR_COL = '#D62828'
CONFIRM_COL = '#2FDD92'

def button_template(id, text, bg_color=None):
  return dbc.Button(
    id=id, 
    children=text, 
    style={'borderRadius': '25px', 'width':'125px', 'background-color': bg_color},
    n_clicks=0, 
    color='info'
  )

INCOME_SAVE = button_template('income-save', 'Save')

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
    button_template('income-empty', 'New Data')
  ],
  # positions upload and new data button to middle of screen
  style={
    'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
    'position': 'absolute', 'top': '50%', 'left': '50%',
    'transform': 'translate(-50%, -50%)'
  },
  hidden=True
)

income_page_size = dbc.InputGroup(
  children=[
    dbc.Input(
      id='income-size', 
      style={'border-radius': '25px 0 0 25px'}, 
      type='number', 
      min=1
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
        dbc.Col(income_page_size, align='end', width='auto'),    
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
        dbc.Col(button_template('income-add', 'Add Row', MAIN_COL), width='auto'),
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

def dropdown_template(id, title):
  return html.Div([
    html.H3(id=id, children=title, style={'margin-top': '10px'}),
    dbc.InputGroup(
    children=[ # settinc is settings + income
      dbc.Input(id=id+'-input', type='text'),
      dbc.Button(id=id+'-button', children='Add', style={'background-color': MAIN_COL}, n_clicks=0),
    ],
    style={'margin-left': '50px'},
    size='sm'
    ),
    dash_table.DataTable(
      id=id+'-tbl',
      style_header = {'display': 'none'},
      row_deletable=True
    )
  ],
  style={'width': '450px'}
  )

nav_square = dbc.Nav(
  children=[
    dbc.NavLink('Page Size', style={'color': 'white'}, href="#sett-page", external_link=True),
    dbc.NavLink('Type of Income', style={'color': 'white'}, href="#sett-inc", external_link=True),
    dbc.NavLink('Type of Expense', style={'color': 'white'}, href="#sett-exp", external_link=True),
    dbc.NavLink('Type of Loan', style={'color': 'white'}, href="#sett-loan", external_link=True),
    dbc.NavLink('Type of Payment', style={'color': 'white'}, href="#sett-mop", external_link=True),
    dbc.NavLink('Export', style={'color': 'white'}, href="#export", external_link=True),
    dbc.NavLink('Delete', style={'color': 'white'}, href="#delete", external_link=True),
  ],
  style={
    'position': 'fixed', 'top': '200px', 'right': '50px',
    'background-color': MAIN_COL, 'width': '200px'
  },
  vertical=True
)

settings_layout = html.Div([
  html.H3(id='sett-page', children='Default Page Size', style={'margin-top': '10px'}),
  dbc.Input(
    id='sett-size', 
    style={'margin-left': '50px', 'width': '400px'}, 
    type='number', 
    min=1, 
    size='sm'
  ),
  dropdown_template('sett-inc', 'Type of Income'),
  dropdown_template('sett-exp', 'Type of Expense'),
  dropdown_template('sett-loan', 'Type of Loan'),
  dropdown_template('sett-mop', 'Payment Method'),
  html.H3(id='export', children='Export Data', style={'margin-top': '10px', 'color': CONFIRM_COL}),
  dbc.Row([
      dbc.Col([button_template('export-income', 'Income')], width='auto'), 
      dbc.Col([button_template('export-expense', 'Expense')], width='auto')
    ],
    style={'width': '450px'},
    justify='evenly'
  ),
  html.H3(id='delete', children='Delete Data', style={'margin-top': '10px', 'color': ERROR_COL}),
  dbc.Row([
      dbc.Col([button_template('delete-income', 'Income')], width='auto'), 
      dbc.Col([button_template('delete-expense', 'Expense')], width='auto')
    ],
    style={'width': '450px'},
    justify='evenly'
  ),
  nav_square
],
style={'margin-left': '50px', 'margin-bottom': '50px'}
)
