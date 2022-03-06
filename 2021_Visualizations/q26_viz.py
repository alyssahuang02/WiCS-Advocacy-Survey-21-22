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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
q_id = 'Q26'


app.layout = html.Div([

    html.Div([
        html.H1('Explore'),
        html.P('Explore the experiences of Harvard undergraduate students with computer science, as they relate to gender and other aspects of identity.')
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
    # get relevant dataframe according to axis
    dff = D.AXIS_DF[axis]

    unique_categories = dff[axis].unique()
    category_names = list(dff[axis].unique())
    
    new_category = []
    
    for c in unique_categories:
        category_df = dff[dff[axis] == c]
        new_category.append(category_df)
 
    generateSpecs = [[{"type": "pie"} for _ in new_category]]
    fig = make_subplots(rows=1, cols=len(new_category),specs = generateSpecs, subplot_titles = category_names)
    colNum = 1
   
    text_annotations=[]
    text_annotations.append(dict(font=dict(size=14)))

    for df in new_category: #new category = inc. in colnum
        yes_num = df[df[q_id].str.contains('Yes', na=False)].shape[0] #filters out yes respondents 
        no_num = df[~(df[q_id].str.contains('Yes', na=False))].shape[0] #filters our no respondents
        y_n_values = [yes_num,no_num]
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
        title='Have you ever been involved in a student organization at Harvard relating to computer science, engineering, or technology?',
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

    # check for errors
    if fig == None or is_sample_size_insufficient(dff, axis):
        print("ERROR")
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
