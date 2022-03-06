import constants as C
import dataframe_init as D

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# response options from survey to question 17
Q12_OPTIONS = [
    'CS 1: Great Ideas in Computer Science',
    'CS 10: Elements of Data Science',
    'CS 20: Discrete Mathematics for Computer Science',
    'CS 50: Introduction to Computer Science I',
    'CS 51: Introduction to Computer Science II',
    'CS 61: Systems Programming and Machine Organization',
    'CS 121: Introduction to Theoretical Computer Science',
    'CS 124: Data Structures and Algorithms',
    'CS 9x, an undergraduate-level research CS course',
    'CS 12x, an undergraduate-level theoretical CS course (other than CS 121 or CS 124)',
    'CS 13x, an undergraduate-level economics/computation course',
    'CS 14x, an undergraduate-level networks course',
    'CS 15x, an undergraduate-level programming languages course',
    'CS 16x, an undergraduate-level systems course',
    'CS 17x, an undergraduate-level graphics/visualization/user interfaces course',
    'CS 18x, an undergraduate-level artificial intelligence course',
    'CS 10x, an undergraduate-level miscellaneous course',
    'CS 22x, a graduate-level theoretical computer science course',
    'CS 23x, a graduate-level economics/computation course',
    'CS 24x, a graduate-level networks course',
    'CS 25x, a graduate-level programming languages course',
    'CS 26x, a graduate-level systems course',
    'CS 27x, a graduate-level graphics/visualization/user interfaces course',
    'CS 28x, a graduate-level artificial intelligence course',
    'CS 20x, a graduate-level miscellaneous course'
]

# categories of courses for visualization
COURSE_CATEGORIES = [
    'CS50: Introduction to Computer Science I',
    'CS51: Introduction to Computer Science II',
    'CS61: Systems Programming and Machine Organization',
    'CS0xx, an introductory undergraduate-level course (other than CS50, CS51, CS61)',
    'CS1xx, an undergraduate-level course',
    'CS2xx, a graduate-level course'
]

# app configuration
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
            value='CS50: Introduction to Computer Science I',
            optionHeight = 70
        )
    ])
], style={'width': '20%', 'display': 'inline-table', 'margin-top' : 20, 'margin-left' : 50}),
    dcc.Graph(id='visualization')
])

# checks if the sample size is sufficient to be displayed
def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return all(c < C.MIN_SAMPLE_SIZE for c in category_counts)

# creates a dictionary mapping the categories of the given axis to the number of survey responders of that axis
# for the given course category
# @params: given a list of dataframes each corresponding to the data pertaining to one category of the given axis
def create_dict(course, df_list, keys):
    dict_final = {}
    length = len(df_list)
    for i in range(length):
        dict_final[keys[i]] = 0

    if course == COURSE_CATEGORIES[0]:
        for i in range(length):
            dict_final[keys[i]] += len(df_list[i].loc[df_list[i]['Q12'].str.contains(Q12_OPTIONS[4], na = False)])
    elif course == COURSE_CATEGORIES[1]:
        for i in range(length):
            dict_final[keys[i]] += len(df_list[i].loc[df_list[i]['Q12'].str.contains(Q12_OPTIONS[5], na = False)])
    elif course == COURSE_CATEGORIES[2]:
        for i in range(length):
            dict_final[keys[i]] += len(df_list[i].loc[df_list[i]['Q12'].str.contains(Q12_OPTIONS[6], na = False)])
    elif course == COURSE_CATEGORIES[3]:
        for j in range(4):
            for i in range(length):
                dict_final[keys[i]] += len(df_list[i].loc[df_list[i]['Q12'].str.contains(Q12_OPTIONS[j], na = False)])
    elif course == COURSE_CATEGORIES[4]:
        for j in range(7, 18):
            for i in range(length):
                dict_final[keys[i]] += len(df_list[i].loc[df_list[i]['Q12'].str.contains(Q12_OPTIONS[j], na = False)])
    else:
        for j in range(18, len(Q12_OPTIONS)):
            for i in range(length):
                dict_final[keys[i]] += len(df_list[i].loc[df_list[i]['Q12'].str.contains(Q12_OPTIONS[j], na = False)])

    return dict_final

@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'),
    Input('course', 'value'))
def update_graph(axis, course):        
    # get relevant dataframe according to axis
    dff = D.AXIS_DF[axis]
    keys = dff[axis].unique()

    df_list = []
    for key in keys:
        df_list.append(dff.loc[dff[axis] == key])
    
    dict_df = create_dict(course, df_list, keys)
    # print(dict_df)
    
    total = 0
    for key in dict_df:
        total += dict_df[key]
    
    percentages = {}
    # fills dict and deals with leftovers
    if not total == 0:
        new_total = 0
        leftovers = {}
        for key in dict_df:
            percentages[key] = round(100*dict_df[key]/total)
            new_total = percentages[key]
            leftovers[key] = 100*dict_df[key]/total - percentages[key]
        if new_total != 100:
            # it must be 99
            key_max = max(leftovers.keys(), key=(lambda k: leftovers[k]))
            percentages[key_max] += 1
    else:
        return C.EMPTY_FIGURE
    
    # print(percentages)

    x_axis = []
    y_axis = []
    size = []
    category = []

    key_index = 0
    
    # ensures legend always shows up
    for key in keys:
        x_axis.append(0)
        y_axis.append(0)
        size.append(0.0000001) # ensures additional circles do not show up on graph
        category.append(key)

    # creates dataframe for scatter plot
    for col in range(10):
        for row in range(10):
            x_axis.append(row)
            y_axis.append(9-col)
            size.append(90)
            while percentages[keys[key_index]] == 0:
                key_index = min(key_index + 1, len(keys))
            category.append(keys[key_index])
            percentages[keys[key_index]] -= 1

    df = pd.DataFrame({'x_axis': x_axis, 'y_axis': y_axis, 'size': size, 'category': category}, index = list(range(100+len(keys))))
    
    # formats figure
    fig = px.scatter(df, x='x_axis', y='y_axis', size='size', color='category')
    fig.update_traces(hovertemplate=None, hoverinfo='skip')
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(width=725, height=650, legend_title='', margin = dict(t=130))
    fig.update_layout(legend=dict(
        orientation="h",
        itemsizing = 'constant',
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font = dict(
            size=9
        ),
    ))

    # adds and configures title
    text = D.QUESTION_KEY['Q12'][0]
    import textwrap
    split_text = textwrap.wrap(text, width=50)
    fig.update_layout(
        title={
            'text': '<br>'.join(split_text),
            'y':0.91,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    # return empty plot if there is not enough data (or if figure is not yet implemented)
    if fig == None or is_sample_size_insufficient(dff, axis):
        return C.EMPTY_FIGURE

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)