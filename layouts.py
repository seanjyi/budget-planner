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

'''Helper function for button template'''
def button_template(id, text, bg_color=None):
  return dbc.Button(
    id=id, 
    children=text, 
    style={'borderRadius': '25px', 'width':'125px', 'background-color': bg_color},
    n_clicks=0, 
    color='info'
  )

INCOME_SAVE = button_template('income-save', 'Save')
EXPENSE_SAVE = button_template('expense-save', 'Save')

INCOME_EXPORT = button_template('export-income', 'Income')
EXPENSE_EXPORT = button_template('export-expense', 'Expense')

INCOME_DELETE = button_template('delete-income', 'Income')
EXPENSE_DELETE = button_template('delete-expense', 'Expense')

# HOME PAGE 

'''Home page layout'''
home_layout = html.Div([html.H1('HOME: UNDER CONSTRUCTION')])

# TRANSACTION HELPER FUNCTIONS
'''Helper function to create new page layout'''
def transaction_new(name):
  return html.Div(
    id=f'{name}-new',
    children=[
      html.Div(
        id=f'{name}-upload-error', 
        children='Selected file type must be CSV',
        style={'color': ERROR_COL},
        hidden=True
      ),
      dcc.Upload(
        id=f'{name}-upload',
        children=html.Div(['Drag and Drop or Select CSV']),
        style={
          'width': '400px', 'height': '60px', 'lineHeight': '60px',
          'borderWidth': '1px', 'borderStyle': 'dashed',
          'borderRadius': '50px', 'textAlign': 'center'
        }
      ),
      html.Plaintext('or'),
      button_template(f'{name}-empty', 'New Data')
    ],
    # positions upload and new data button to middle of screen
    style={
      'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
      'position': 'absolute', 'top': '50%', 'left': '50%',
      'transform': 'translate(-50%, -50%)'
    }
  )

'''Helper function to create page size layout'''
def transaction_page(name):
  return dbc.InputGroup(
    children=[
      dbc.Input(
        id=f'{name}-size', 
        style={'border-radius': '25px 0 0 25px'}, 
        type='number', 
        min=1
      ),
      dbc.Button(
        id=f'{name}-page', 
        children='Page Size', 
        style={'border-radius': '0 25px 25px 0', 'background-color': MAIN_COL}, 
        n_clicks=0
      ),
    ],
    style={'width': '180px', 'margin-right': '10px', 'margin-bottom': '10px'},
    size='sm'
  )

# INCOME PAGE

'''New income page layout'''
income_new = transaction_new('income')

'''Income database table layout'''
income_data = html.Div(
  id='income-data',
  children=[
    # title and page size control
    dbc.Row(
      children=[
        dbc.Col(html.H1('Income', style={'text-align': 'center'})),
        dbc.Col(),
        dbc.Col(transaction_page('income'), align='end', width='auto'),    
      ],
      style={'margin-top': '10px'}
    ),
    dash_table.DataTable(
      id='income-tbl',
      columns=[
        {'id': 'date', 'name': 'Date (YYYY-MM-DD)', 'type': 'datetime'}, 
        {'id': 'category', 'name': 'Category', 'presentation': 'dropdown'},
        {'id': 'amount', 'name': 'Amount ($)', 'type': 'numeric', 'format': Format(precision=2, symbol=Symbol.yes, scheme=Scheme.fixed).group(True)}, 
        {'id': 'mop', 'name': 'MOP', 'presentation': 'dropdown'},
        {'id': 'repay', 'name': 'Repayment', 'presentation': 'dropdown'}
      ],
      style_cell={'text-align': 'center'},
      style_data={
        'height': 'auto',
        'lineHeight': '15px'
      },
      editable=True,
      row_deletable=True
    ),
    html.Div(
      id='income-tbl-error', 
      children='Incomplete income & payment dropdown lists:\nGo to Settings and finish lists',
      style={'color': ERROR_COL, 'whiteSpace': 'pre-wrap', 'margin': '10px'},
      hidden=True
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
  ]
) 

'''Income page layout'''
income_layout = html.Div(id='income-content', children=[income_new])

# EXPENSE PAGE

'''New expense page layout'''
expense_new = transaction_new('expense')

'''Expense database table layout'''
expense_data = html.Div(
  id='expense-data',
  children=[
    # title and page size control
    dbc.Row(
      children=[
        dbc.Col(html.H1('Expense', style={'text-align': 'center'})),
        dbc.Col(),
        dbc.Col(transaction_page('expense'), align='end', width='auto'),    
      ],
      style={'margin-top': '10px'}
    ),
    dash_table.DataTable(
      id='expense-tbl',
      columns=[
        {'id': 'date', 'name': 'Date (YYYY-MM-DD)', 'type': 'datetime'}, 
        {'id': 'place', 'name': 'Place', 'type': 'text'},
        {'id': 'amount', 'name': 'Amount ($)', 'type': 'numeric', 'format': Format(precision=2, symbol=Symbol.yes, scheme=Scheme.fixed).group(True)}, 
        {'id': 'mop', 'name': 'MOP', 'presentation': 'dropdown'},
        {'id': 'category', 'name': 'Category', 'presentation': 'dropdown'}
      ],
      style_cell={'text-align': 'center'},
      style_data={
        'height': 'auto',
        'lineHeight': '15px'
      },
      editable=True,
      row_deletable=True
    ),
    html.Div(
      id='expense-tbl-error', 
      children='Incomplete expense & payment dropdown lists:\nGo to Settings and finish lists',
      style={'color': ERROR_COL, 'whiteSpace': 'pre-wrap', 'margin': '10px'},
      hidden=True
    ),
    # positions add and save button
    dbc.Row(
      [
        dbc.Col(button_template('expense-add', 'Add Row', MAIN_COL), width='auto'),
        dbc.Col(id='expense-button', children=INCOME_SAVE, width='auto'),
      ],
      style={'margin-top': '50px'},
      justify='evenly'
    ),
  ]
) 

'''Expense page layout'''
expense_layout = html.Div(id='expense-content', children=[expense_new])

# SETTINGS PAGE

'''Helper function for dropdown layouts'''
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

'''Settings page navigation tab'''
nav_square = dbc.Nav(
  children=[
    dbc.NavLink('Page Size', style={'color': 'white'}, href="#sett-page", external_link=True),
    dbc.NavLink('Type of Income', style={'color': 'white'}, href="#sett-inc", external_link=True),
    dbc.NavLink('Type of Expense', style={'color': 'white'}, href="#sett-exp", external_link=True),
    dbc.NavLink('Type of Loan', style={'color': 'white'}, href="#sett-loan", external_link=True),
    dbc.NavLink('Type of Payment', style={'color': 'white'}, href="#sett-pay", external_link=True),
    dbc.NavLink('Export', style={'color': 'white'}, href="#export", external_link=True),
    dbc.NavLink('Delete', style={'color': 'white'}, href="#delete", external_link=True),
  ],
  style={
    'position': 'fixed', 'top': '200px', 'right': '50px',
    'background-color': MAIN_COL, 'width': '200px'
  },
  vertical=True
)

'''Settings page layout'''
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
  dropdown_template('sett-pay', 'Method of Payment'),
  html.H3(id='export', children='Export to CSV file', style={'margin-top': '10px', 'color': CONFIRM_COL}),
  dbc.Row([
      dbc.Col(id='export-inc-button', children=INCOME_EXPORT, width='auto'), 
      dbc.Col(id='export-exp-button', children=EXPENSE_EXPORT, width='auto')
    ],
    style={'width': '450px'},
    justify='evenly'
  ),
  html.H3(id='delete', children='Delete Dataset', style={'margin-top': '10px', 'color': ERROR_COL}),
  dbc.Row([
      dbc.Col(id='delete-inc-button', children=INCOME_DELETE, width='auto'), 
      dbc.Col(id='delete-exp-button', children=EXPENSE_DELETE, width='auto')
    ],
    style={'width': '450px'},
    justify='evenly'
  ),
  nav_square
],
style={'margin-left': '50px', 'margin-bottom': '50px'}
)
