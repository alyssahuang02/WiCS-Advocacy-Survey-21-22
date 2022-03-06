# color scheme

import constants as C
import dataframe_init as D

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc


# constants
# column titles with formatting
COLUMN_TITLES = ['', 'My first-year <br> academic advisor <br> <br>', 'Residential advising <br> Resources, such as <br> house tutors <br> or proctors <br> <br>',
                 'Department <br> heads <br> <br>', 'Department <br> faculty <br> <br>', 'Department-specific <br> advising programs <br> <br>', 
                 'Peer <br> Advising <br> Fellows (PAFs) <br> <br>']

# label names used to extract data
ANSWER_OPTIONS = ['My first-year academic advisor', 'Residential advising resources, such as house tutors or proctors',
                  'Department heads',  'Department faculty', 'Department-specific advising programs', 
                  'Peer Advising Fellows (PAFs)']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([

    html.Div([
        html.H1('Explore'),
        html.P('Which of the following on-campus resources have helped you decide your concentration(s)?')
    ], style={'width': '30%', 'display': 'inline-table', 'margin-top': 60, 'margin-left': 50}),
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
    ], style={'width': '20%', 'display': 'inline-table', 'margin-top': 20, 'margin-left': 50}),
    html.Div(
        children=[
            dcc.Graph(id='visualization')
        ],
        style={'margin-top': 40, 'margin-right': 90,
               'justify-content': 'center'}
    ),

])


def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')[
        'counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)

@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'))
def update_graph(axis):
    # extract relevant data
    dff = D.AXIS_DF[axis]
    columnOptions = []
    for choice in ANSWER_OPTIONS:
        columnOptions.append(dff[dff['Q5'].str.contains(
            choice, na=False)])
            
    # names is used for labelling
    names = list(dff[axis].unique())

    # initialize subplot
    generateSpecs = [[{"type": "pie"}
                      for _ in range(len(columnOptions)+1)] for _ in names]
    figSub = make_subplots(rows=len(names), cols=len(
        columnOptions)+1, specs=generateSpecs, column_titles=COLUMN_TITLES)
    rowNum = 1

    for label in names:
        colNum = 1
        figSub.add_trace(go.Table(
            header=dict(values=[label], fill_color='rgba(0,0,0,0)'),
            cells=dict(values=[' '],
                       fill_color='rgba(0,0,0,0)',
                       align='center')
        ), row=rowNum, col=colNum)
        colNum += 1

        # construct pie chart
        for colOption in columnOptions:

            votes = [0, 0]
            for x in colOption[axis]:
                if x == label:
                    votes[0] += 1

            total = dff[dff[axis] == label]['Q5'].count()

            votes[1] = total - votes[0]
            figSub.add_trace(go.Pie(labels=['Yes', 'No'], values=votes, textinfo='none',
                                    hoverinfo='label+percent',
                                    marker={
                'colors': [
                                    'rgb(71,159,118)',
                                    'rgb(233,236,239)']}), row=rowNum, col=colNum)

            colNum += 1
        rowNum += 1
        # print(total)

    text_annotations=[]
    text_annotations.append(dict(font=dict(size=14)))
    # check for errors
    if figSub == None or is_sample_size_insufficient(dff, axis):
        print("ERROR")
        return C.EMPTY_FIGURE
    # plot titles
    figSub.update_layout(
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
    return figSub


if __name__ == '__main__':
    app.run_server(debug=True)