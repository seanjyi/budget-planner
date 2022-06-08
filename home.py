'''
Main file for the program. Creates the application frame,
and also handles multiple page navigation.
'''

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
import income
from layouts import home_layout, settings_layout, expense_layout, income_layout

INIT_PAGE_SIZE = 10

'''Navigation bar layout'''
navbar = dbc.NavbarSimple(
  dbc.Row([
      dbc.Col(dbc.NavItem(dbc.NavLink("Github", href="https://github.com/seanjyi/budget-planner"))),
      dbc.Col(dbc.NavItem(dbc.NavLink("Income", href="/income"))),
      dbc.Col(dbc.NavItem(dbc.NavLink("Expense", href="/expense"))),
      dbc.Col(dbc.NavItem(dbc.NavLink(html.Img(src='assets/gear.png', height='30px'), href="/settings")))
    ],
    align='center'
  ),
  brand="Finance",
  brand_href="/home",
  color="LightSlateGrey",  # color of navBar
  dark=True
)

'''Main app layout'''
app_layout = html.Div([
  navbar,
  dcc.Location(id='url', refresh=False),
  dcc.Store(id='page-size', data=INIT_PAGE_SIZE),  # remembers init_page during user session
  dcc.Store(id='income-tbl-data', storage_type='memory'),  # remmeber dcc store bug
  html.Div(id='page-content')
])

'''Handles multi-page navigation'''
@callback(
  Output('page-content', 'children'),
  Output('url', 'pathname'),
  Input('url', 'pathname')
)
def display_page(pathname):
  if pathname == '/income':
    return income_layout, '/income'
  elif pathname == '/expense':
    return expense_layout, '/expense'
  elif pathname == '/settings':
    return settings_layout, '/settings'
  else:
    return home_layout, '/home'

'''Initalizes dash application, uses LUX theme and supresses callback'''
if __name__ == '__main__':
  app = Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)

  app.title = 'Budget Planner'
  app.layout = app_layout

  income.income_init()

  app.run_server(debug=True, use_reloader=False)  # reloader = false for debugging
