# for now, no change, but flag as q for later

import constants as C
import dataframe_init as D

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

legend_labels = ['1', '2', '3', '4', '5', '6', '7']
bar_colors = ['rgba(102, 0, 0, 0.8)', 'rgba(204, 0, 0, 0.8)', 'rgba(234, 153, 153, 0.8)', 'rgba(217, 217, 217, 0.8)', 'rgba(164, 194, 244, 0.8)', 'rgba(60, 120, 216, 0.8)', 'rgba(28, 69, 135, 0.8)']
#QUESTION_ID = 'Q7_1'

# categories of courses for visualization
COURSE_CATEGORIES = {
    'Computer Programming':'Q7_1', 'Theoretical computer science':'Q7_2', 'Economics and computation':'Q7_3',
    'Networks':'Q7_4', 'Programming languages':'Q7_5', 'Formal Reasoning':'Q7_6', 'Systems':'Q7_7',
    'Graphics, visualization, and user interfaces':'Q7_8', 'Artificial intelligence':'Q7_9'
}

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
        html.H4('Course'),
        html.Div([
            dcc.Dropdown(
                id='course',
                options=[{'label': i, 'value': i} for i in COURSE_CATEGORIES],
                value='Computer Programming',
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

def calculate_percentages(dff, axis, y_data, QUESTION_ID):
    data = []
    for y_label in y_data:
        filt_dff = dff[dff[axis] == y_label]
        eval_counts = []
        total = 0
        row = []
        for eval_label in legend_labels:
            count = filt_dff[filt_dff[QUESTION_ID] == eval_label].shape[0]
            eval_counts.append(count)
            total += count
        for count in eval_counts:
            value = 0
            if total != 0:
                value = round(count * 100 / total, 2)
            row.append(value)
        data.append(row)
        # print(y_label + ": " + str(total))
    return data

@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'),
    Input('course', 'value'))
def update_graph(axis, course):
    
    QUESTION_ID = COURSE_CATEGORIES[course]

    dff = D.AXIS_DF[axis]

    fig = go.Figure()
    y_data = dff[axis].unique()[::-1]
    x_data = calculate_percentages(dff, axis, y_data, QUESTION_ID)

    # return empty plot if there is not enough data (or if figure is not yet implemented)
    if fig == None or is_sample_size_insufficient(dff, axis):
        return C.EMPTY_FIGURE

    for row in range(len(x_data)):
        for col in range(len(x_data[0])):
            hovertext = str(x_data[row][col]) + '% - ' + legend_labels[col]
            fig.add_trace(go.Bar(
                x=[x_data[row][col]], y=[row],
                orientation='h',
                hoverinfo='text',
                hovertext=hovertext,
                marker=dict(
                    color=bar_colors[col],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=0, r=0, t=140, b=80),
        showlegend=False
    )

    annotations = []
    for i in range(len(y_data)):
        # labeling the y-axis
        split_label = textwrap.wrap(str(y_data[i]), width=18)
        annotations.append(dict(xref='paper', yref='y',
                                x=0.13, y=i,
                                xanchor='right',
                                text='<br>'.join(split_label),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))

    split_text = textwrap.wrap(D.QUESTION_KEY[QUESTION_ID][0], width=100)
    fig.update_layout(annotations=annotations, title_text='<br>'.join(split_text))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)