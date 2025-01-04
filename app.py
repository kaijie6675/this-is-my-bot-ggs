import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import subprocess
import psutil
import pandas as pd
import plotly.graph_objs as go
import base64
import io
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Trading Bot Configuration"),
    
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Backtest', children=[
            html.H2("Backtest Settings"),
            html.Label("Select Backtest Strategy:"),
            dcc.Dropdown(
                id='backtest-strategy-dropdown',
                options=[
                    {'label': 'DDPG', 'value': 'DDPG'},
                    {'label': 'Quantitative', 'value': 'Quantitative'},
                    {'label': 'Mean Reversion', 'value': 'MeanReversion'},
                    {'label': 'Moving Average Crossover', 'value': 'MovingAverageCrossover'},
                    {'label': 'Quantitative Scalping', 'value': 'QuantitativeScalping'}
                ],
                value='Quantitative'
            ),
            html.Br(),
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='backtest-date-picker',
                start_date=datetime.date(2025, 1, 1),
                end_date=datetime.date(2025, 1, 4),
                display_format='YYYY-MM-DD'
            ),
            html.Br(),
            dcc.Upload(
                id='upload-backtest-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True
            ),
            html.Button('Start Backtest', id='start-backtest-button'),
            html.Div(id='backtest-output-container'),
            dcc.Graph(id='backtest-graph')
        ]),
        dcc.Tab(label='RL+ML (Training)', children=[
            html.H2("Reinforcement Learning + Machine Learning (Training) Settings"),
            html.Label("Select RL+ML Strategy:"),
            dcc.Dropdown(
                id='rlml-strategy-dropdown',
                options=[
                    {'label': 'DDPG', 'value': 'DDPG'},
                    {'label': 'Quantitative', 'value': 'Quantitative'},
                    {'label': 'Mean Reversion', 'value': 'MeanReversion'},
                    {'label': 'Moving Average Crossover', 'value': 'MovingAverageCrossover'},
                    {'label': 'Quantitative Scalping', 'value': 'QuantitativeScalping'},
                    {'label': 'DDPG Training', 'value': 'DDPG_Training'}
                ],
                value='Quantitative'
            ),
            html.Br(),
            dcc.Upload(
                id='upload-rlml-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True
            ),
            html.Button('Start RL+ML Bot', id='start-rlml-button'),
            html.Div(id='rlml-output-container')
        ]),
        dcc.Tab(label='Paper Trade', children=[
            html.H2("Paper Trade Settings"),
            html.Label("Select Paper Trade Strategy:"),
            dcc.Dropdown(
                id='paper-trade-strategy-dropdown',
                options=[
                    {'label': 'DDPG', 'value': 'DDPG'},
                    {'label': 'Quantitative', 'value': 'Quantitative'},
                    {'label': 'Mean Reversion', 'value': 'MeanReversion'},
                    {'label': 'Moving Average Crossover', 'value': 'MovingAverageCrossover'},
                    {'label': 'Quantitative Scalping', 'value': 'QuantitativeScalping'}
                ],
                value='Quantitative'
            ),
            html.Br(),
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='paper-trade-date-picker',
                start_date=datetime.date(2025, 1, 1),
                end_date=datetime.date(2025, 1, 4),
                display_format='YYYY-MM-DD'
            ),
            html.Br(),
            dcc.Upload(
                id='upload-paper-trade-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True
            ),
            html.Button('Start Paper Trade Bot', id='start-paper-trade-button'),
            html.Div(id='paper-trade-output-container')
        ]),
        dcc.Tab(label='Statistics', children=[
            html.H2("Statistics"),
            html.Div(id='stats-output')
        ]),
        dcc.Tab(label='Performance', children=[
            html.H2("Performance"),
            # Add performance components here
        ]),
        dcc.Tab(label='PC Usage', children=[
            html.H2("PC Usage"),
            dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
            html.Div(id='pc-usage')
        ]),
    ])
])

@app.callback(
    [Output('backtest-output-container', 'children'),
     Output('backtest-graph', 'figure')],
    [Input('start-backtest-button', 'n_clicks'),
     Input('backtest-strategy-dropdown', 'value'),
     Input('backtest-date-picker', 'start_date'),
     Input('backtest-date-picker', 'end_date')],
    [State('upload-backtest-data', 'contents'),
     State('upload-backtest-data', 'filename')]
)
def start_backtest(n_clicks, selected_strategy, start_date, end_date, contents, filename):
    if n_clicks is not None and contents is not None:
        # Process file contents and generate graph
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        # Make sure 'time' and 'portfolio' columns exist
        if 'time' in df.columns and 'portfolio' in df.columns:
            fig = {
                'data': [{
                    'x': df['time'],
                    'y': df['portfolio'],
                    'type': 'line'
                }],
                'layout': {
                    'title': 'Backtest Results',
                    'xaxis': {'title': 'Time'},
                    'yaxis': {'title': 'Portfolio'}
                }
            }
            # Start the backtest process
            subprocess.Popen(['python', 'main.py', selected_strategy, start_date, end_date])
            return "", fig
        else:
            return "The uploaded file does not contain 'time' and 'portfolio' columns.", {}
    else:
        return ("Run Backtest for Graph", {})

@app.callback(
    Output('rlml-output-container', 'children'),
    Input('start-rlml-button', 'n_clicks'),
    Input('rlml-strategy-dropdown', 'value'),
    State('upload-rlml-data', 'contents'),
    State('upload-rlml-data', 'filename')
)
def start_rlml(n_clicks, selected_strategy, contents, filename):
    if n_clicks is not None:
        # Start the RL+ML bot with the selected strategy
        subprocess.Popen(['python', 'main.py', selected_strategy])
        return f"Started RL+ML bot with strategy: {selected_strategy}"

@app.callback(
    Output('paper-trade-output-container', 'children'),
    Input('start-paper-trade-button', 'n_clicks'),
    Input('paper-trade-strategy-dropdown', 'value'),
    Input('paper-trade-date-picker', 'start_date'),
    Input('paper-trade-date-picker', 'end_date'),
    State('upload-paper-trade-data', 'contents'),
    State('upload-paper-trade-data', 'filename')
)
def start_paper_trade(n_clicks, selected_strategy, start_date, end_date, contents, filename):
    if n_clicks is not None:
        # Start the paper trade bot with the selected strategy
        subprocess.Popen(['python', 'main.py', selected_strategy, start_date, end_date])
        return f"Started paper trade bot with strategy: {selected_strategy}"

@app.callback(
    Output('pc-usage', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_pc_usage(n):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    return f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
