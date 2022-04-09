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

gender_dict = {'Nonmales':81, 'Males':21}
gender_label = list(gender_dict.keys())
gender_num = list(gender_dict.values())

fig = px.bar(x = gender_label, y = gender_num)

app.layout = html.Div([
    html.Div([
        dcc.Graph(figure=fig)
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)