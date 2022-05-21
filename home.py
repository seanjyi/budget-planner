from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import income, expense

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.config['suppress_callback_exceptions'] = True
server = app.server

INIT_PAGE_SIZE = 15

navbar = dbc.NavbarSimple(
  children=[
    dbc.NavItem(dbc.NavLink("Github", href="https://github.com/seanjyi/budget-planner")),
    dbc.NavItem(dbc.NavLink("Income", href="/income")),
    dbc.NavItem(dbc.NavLink("Expense", href="/expense")),
  ],
  brand="Finance",
  brand_href="/home",
  color="LightSlateGrey", # color of navBar  
  dark=True,
)

app.layout = html.Div([
  navbar,
  dcc.Location(id='url', refresh=False),
  dcc.Store(id='page-size', data=INIT_PAGE_SIZE),
  html.Div(id='page-content')
])

home_layout = html.Div([
  html.H1('HOME: UNDER CONSTRUCTION')
])

# Other than income and expense, autocorrects pathname to '/home'
@app.callback(
  Output('page-content', 'children'),
  Output('url', 'pathname'),
  Input('url', 'pathname')
)
def display_page(pathname):
  if pathname == '/income':
    return income.layout, '/income'
  elif pathname == '/expense':
    return expense.layout, '/expense'
  else:
    return home_layout, '/home'

if __name__ == '__main__':
  app.run_server(debug=True)
