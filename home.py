'''
Main file for the program. Creates the application frame,
and also handles multiple page navigation.
'''

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import income, expense, settings
import time

INIT_PAGE_SIZE = 10

'''Initalizes dash application, uses LUX theme and supresses callback'''
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
# app.config['suppress_callback_exceptions'] = True
server = app.server

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
  color="LightSlateGrey", # color of navBar  
  dark=True
)

'''Main app layout'''
app.title = 'Budget Planner'
app.layout = html.Div([
  navbar,
  dcc.Location(id='url', refresh=False),
  dcc.Store(id='page-size', data=INIT_PAGE_SIZE), # remembers init_page during user session
  html.Div(id='page-content')
])

home_layout = html.Div([
  html.H1('HOME: UNDER CONSTRUCTION')
])

'''Handles multi-page navigation'''
@callback(
  Output('page-content', 'children'),
  Output('url', 'pathname'),
  Input('url', 'pathname')
)
def display_page(pathname):
  if pathname == '/income':
    return income.layout, '/income'
  elif pathname == '/expense':
    return expense.layout, '/expense'
  elif pathname == '/settings':
    return settings.layout, '/settings'
  else:
    return home_layout, '/home'  

if __name__ == '__main__':
  app.run_server(debug=True) 
