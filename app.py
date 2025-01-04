import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import subprocess

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Trading Bot Configuration"),
    
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Backtest', children=[
            html.H2("Backtest Settings"),
            # Dropdown for selecting strategy
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
                value='DDPG'  # Default value
            ),
            html.Br(),
            # Button to start the backtest
            html.Button('Start Backtest', id='start-backtest-button'),
            # Placeholder for output
            html.Div(id='backtest-output-container')
        ]),
        dcc.Tab(label='RL+ML', children=[
            html.H2("Reinforcement Learning + Machine Learning Settings"),
            # Dropdown for selecting strategy
            html.Label("Select RL+ML Strategy:"),
            dcc.Dropdown(
                id='rlml-strategy-dropdown',
                options=[
                    {'label': 'DDPG', 'value': 'DDPG'},
                    {'label': 'Quantitative', 'value': 'Quantitative'},
                    {'label': 'Mean Reversion', 'value': 'MeanReversion'},
                    {'label': 'Moving Average Crossover', 'value': 'MovingAverageCrossover'},
                    {'label': 'Quantitative Scalping', 'value': 'QuantitativeScalping'}
                ],
                value='DDPG'  # Default value
            ),
            html.Br(),
            # Button to start the RL+ML bot
            html.Button('Start RL+ML Bot', id='start-rlml-button'),
            # Placeholder for output
            html.Div(id='rlml-output-container')
        ]),
        dcc.Tab(label='Paper Trade', children=[
            html.H2("Paper Trade Settings"),
            # Dropdown for selecting strategy
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
                value='DDPG'  # Default value
            ),
            html.Br(),
            # Button to start the paper trade bot
            html.Button('Start Paper Trade Bot', id='start-paper-trade-button'),
            # Placeholder for output
            html.Div(id='paper-trade-output-container')
        ]),
        dcc.Tab(label='Statistics', children=[
            html.H2("Statistics"),
            # Add statistics components here
        ]),
        dcc.Tab(label='Performance', children=[
            html.H2("Performance"),
            # Add performance components here
        ]),
        dcc.Tab(label='PC Usage', children=[
            html.H2("PC Usage"),
            # Add PC usage components here
        ]),
    ])
])

# Callback to start the backtest bot
@app.callback(
    Output('backtest-output-container', 'children'),
    Input('start-backtest-button', 'n_clicks'),
    Input('backtest-strategy-dropdown', 'value')
)
def start_backtest(n_clicks, selected_strategy):
    if n_clicks is not None:
        # Start the backtest bot with the selected strategy
        subprocess.Popen(['python', 'main.py', selected_strategy])
        return f"Started backtest with strategy: {selected_strategy}"

# Callback to start the RL+ML bot
@app.callback(
    Output('rlml-output-container', 'children'),
    Input('start-rlml-button', 'n_clicks'),
    Input('rlml-strategy-dropdown', 'value')
)
def start_rlml(n_clicks, selected_strategy):
    if n_clicks is not None:
        # Start the RL+ML bot with the selected strategy
        subprocess.Popen(['python', 'main.py', selected_strategy])
        return f"Started RL+ML bot with strategy: {selected_strategy}"

# Callback to start the paper trade bot
@app.callback(
    Output('paper-trade-output-container', 'children'),
    Input('start-paper-trade-button', 'n_clicks'),
    Input('paper-trade-strategy-dropdown', 'value')
)
def start_paper_trade(n_clicks, selected_strategy):
    if n_clicks is not None:
        # Start the paper trade bot with the selected strategy
        subprocess.Popen(['python', 'main.py', selected_strategy])
        return f"Started paper trade bot with strategy: {selected_strategy}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)