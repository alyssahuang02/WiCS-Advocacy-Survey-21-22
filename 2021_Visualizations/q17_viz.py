import constants as C
import dataframe_init as D

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

from datetime import datetime

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

QUESTION_OPTIONS = [      
    "I didn't learn about opportunities relating to graduate studies until it was too late",
    "I did not feel as if I had the resources to successfully apply to graduate school",
    "Graduate school doesn't fit into my career path"]

QUESTION_ID = 'Q17'


app.layout = html.Div([
html.Div([
    html.H1('Explore'),
    html.P('Explore the experiences of Harvard undergraduate students with computer science, as they relate to gender and other aspects of identity.')
], style={'width': '30%', 'display': 'inline-table', 'margin-top' : 60, 'margin-left' : 50}),
html.Div([
    html.H4('Split by'),
    html.Div([
        dcc.Dropdown(
            id='axis',
            options=[{'label': i, 'value': i} for i in C.VIZ_AXES],
            value='Gender',
            clearable=False
        )
    ])
], style={'width': '20%', 'display': 'inline-table', 'margin-top' : 20, 'margin-left' : 50}),
html.Div([
    html.H4('Answer Options'),
    html.Div([
        dcc.Dropdown(
            id='question_option',
            options=[{'label': i, 'value': i} for i in QUESTION_OPTIONS],
            value=QUESTION_OPTIONS[0],
            optionHeight = 70
        )
    ])
], style={'width': '20%', 'display': 'inline-table', 'margin-top' : 20, 'margin-left' : 50}),
    dcc.Graph(id='visualization')
])

def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)


@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'),
    Input('question_option', 'value'))
def update_graph(axis, question_option):
    # get relevant dataframe according to axis
    dff = D.AXIS_DF[axis]
    
    # names is used for labelling
    names = list(dff[axis].unique())
 
    # implement figure   
    generateSpecs = [[{"type": "pie"} for _ in names]]
    fig = make_subplots(rows=1, cols=len(names), specs = generateSpecs, subplot_titles = names)
    colNum = 1

    for name in names:
        df = dff[dff[axis] == name]
        yes_num = df[df[QUESTION_ID].str.contains(question_option, na=False)].shape[0] #filters out yes respondents 
        no_num = df[~(df[QUESTION_ID].str.contains(question_option, na=False))].shape[0] #filters our no respondents
        y_n_values = [yes_num,no_num]
        # print(name + ": " + str(yes_num + no_num))

        text_annotations=[]
        text_annotations.append(dict(font=dict(size=14)))

        fig.add_trace(go.Pie(
            labels = ['Yes', 'No'],
            values = y_n_values,
            textinfo='none',
            hoverinfo='label+percent',
            direction = 'clockwise',
            sort = False,
            marker={'colors': ['rgb(71,159,118)', 'rgb(233,236,239)']}
        ), row=1, col=colNum)
        colNum +=1
    fig.update_layout(
        title='Which of the following reasons has influenced your decision to ultimately not apply to graduate school?',
        annotations=text_annotations,
        height=300,
        margin=dict(l=0, r=0, t=70, b=30),
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=1.02,
            itemclick=False,
            itemdoubleclick=False
        )
    )

    # return empty plot if there is not enough data (or if figure is not yet implemented)
    if fig == None or is_sample_size_insufficient(dff, axis):
        return C.EMPTY_FIGURE

    return fig
       
if __name__ == '__main__':
    app.run_server(debug=True)