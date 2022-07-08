'''
Main file for the program. Creates the application frame,
and also handles multiple page navigation.
'''

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback
import income
import settings
import layouts

'''Navigation bar layout'''
navbar = dbc.NavbarSimple(
  dbc.Row([
      dbc.Col(dbc.NavItem(dbc.NavLink('Github', href='https://github.com/seanjyi/budget-planner'))),
      dbc.Col(dbc.NavItem(dbc.NavLink('Income', href='/income'))),
      dbc.Col(dbc.NavItem(dbc.NavLink('Expense', href='/expense'))),
      dbc.Col(dbc.NavItem(dbc.NavLink(html.Img(src='assets/gear.png', height='30px'), href='/settings')))
    ],
    align='center'
  ),
  brand='Finance',
  brand_href='/home',
  color=layouts.MAIN_COL,  # color of navBar
  dark=True
)

'''Main app layout'''
app_layout = html.Div([
  navbar,
  dcc.Location(id='url', refresh=False),
  dcc.Store(id='income-tbl-data', storage_type='memory'), # remember dcc.Store storage_type difference
  dcc.Store(id='income-trigger'),
  dcc.Store(id='sett-size-store'),
  dcc.Store(id='sett-inc-store'),
  dcc.Store(id='sett-exp-store'),
  dcc.Store(id='sett-loan-store'),
  dcc.Store(id='sett-pay-store'),
  html.Div(id='page-content')
])

'''Handles multi-page navigation'''
@callback(
  Output('page-content', 'children'),
  Output('url', 'pathname'),
  Input('url', 'pathname'),
  State('income-trigger', 'data')
)
def display_page(pathname, income):
  if pathname == '/income':
    if income == None:
      return layouts.income_layout, '/income'
    else:
      return layouts.income_data, '/income'
  elif pathname == '/expense':
    return layouts.expense_layout, '/expense'
  elif pathname == '/settings':
    return layouts.settings_layout, '/settings'
  else:
    return layouts.home_layout, '/home'

'''Initalizes dash application, uses LUX theme and supresses callback'''
if __name__ == '__main__':
  app = Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)

  app.title = 'Budget Planner'
  app.layout = app_layout

  settings.sett_init()
  income.income_init()
  
  # run use_reloader when :memory: helps for fast debugging
  if settings.DBLOC == ':memory:':
    app.run_server(debug=True, use_reloader=True)
  else:
    app.run_server(debug=True, use_reloader=False)
