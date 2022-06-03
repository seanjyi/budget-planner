'''
Contains all the layouts of the application.
Layouts are all stored here to make individual page code 
easy to read.
'''
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme, Symbol

home_layout = html.Div([
  html.H1('HOME: UNDER CONSTRUCTION')
])

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

input_group = dbc.InputGroup(
  [
    dbc.Input(id='size-input', type='number'),
    dbc.Button(id='page-button', n_clicks=0, children='Page Size'),
  ],
  size='sm',
  style={'width': '180px'}
)

'''Income data table page layout'''
income_layout = html.Div([
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

expense_layout = html.Div([
    html.H3('Warning: Construction Zone')
])

settings_layout = html.Div([
    html.H3('Warning: Construction Zone')
])