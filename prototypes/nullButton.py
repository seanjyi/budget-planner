from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    html.Button('Submit', id='submit-val', n_clicks=0)
])


@app.callback(
    Output('submit-val', 'n_clicks'),
    Input('submit-val', 'n_clicks')
)
def update_output(n_clicks):
    print("hi")
    return n_clicks


if __name__ == '__main__':
    app.run_server(debug=True)
