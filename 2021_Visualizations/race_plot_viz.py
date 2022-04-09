import constants as C
import dataframe_init as D
import matplotlib.pyplot as plt
import mpld3
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import textwrap

import pandas as pd
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

race_dict = {'Asian':73, 'Black or African American':4, 'Hispanic or Latinx':4, 'White':35}
race_label = list(race_dict.keys())
race_num = list(race_dict.values())

fig = px.bar(x = race_label, y = race_num)

app.layout = html.Div([
    html.Div([
        dcc.Graph(figure=fig)
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)