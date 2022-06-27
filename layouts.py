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
      style={'color': '#D62828'},
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
    dbc.Input(id='income-size', style={'border-radius': '25px 0 0 25px'}, type='number'),
    dbc.Button(id='income-page', children='Page Size', style={'border-radius': '0 25px 25px 0', 'background-color': 'LightSlateGrey'}, n_clicks=0),
  ],
  style={'width': '180px', 'margin-right': '10px'},
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
        dbc.Col(dbc.Button(id='income-add', n_clicks=0, children='Add Row', style={'borderRadius': '25px', 'background-color': 'LightSlateGrey'}), width='auto'),
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

settings_layout = html.Div([
  html.H3('Default Page Size'),
  html.H3('Type of Income'),
  html.H3('Type of Expense'),
  html.H3('Type of Loan'),
  html.H3('Payment Method'),
])