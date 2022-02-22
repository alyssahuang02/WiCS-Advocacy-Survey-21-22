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
html.Div([
    html.H4('Filter'),
    dbc.Button("Select Filters", color="info", id="open-filter", className="mr-1"),
    dbc.Modal(
        [
            dbc.ModalHeader("Filter Options"),
            dbc.ModalBody("You may only select up to two filters at a time, and you may not filter on the basis of your selected split."),
            html.Div([
                html.Div([
                    html.P('Gender'),
                    dcc.Dropdown(
                        id='filter-gender-dropdown',
                        options=[{'label': i, 'value': i} for i in C.GENDER_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                html.Div([
                    html.P('Race/Ethnicity'),
                    dcc.Dropdown(
                        id='filter-race-ethnicity-dropdown',
                        options=[{'label': i, 'value': i} for i in C.RACE_ETHNICITY_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
            ]),
            html.Div([
                html.Div([
                    html.P('BGLTQ+'),
                    dcc.Dropdown(
                        id='filter-bgltq-dropdown',
                        options=[{'label': i, 'value': i} for i in C.BGLTQ_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                html.Div([
                    html.P('First Generation, Low Income (FGLI)'),
                    dcc.Dropdown(
                        id='filter-fgli-dropdown',
                        options=[{'label': i, 'value': i} for i in C.FGLI_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
            ]),
            html.Div([
                html.Div([
                    html.P('Class Year'),
                    dcc.Dropdown(
                        id='filter-class-year-dropdown',
                        options=[{'label': i, 'value': i} for i in C.CLASS_YEAR_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                html.Div([
                    html.P('School of Primary Concentration'),
                    dcc.Dropdown(
                        id='filter-school-dropdown',
                        options=[{'label': i, 'value': i} for i in C.SCHOOL_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
            ]),
            html.Div([
                html.Div([
                    html.P('Primary Concentration'),
                    dcc.Dropdown(
                        id='filter-concentration-dropdown',
                        options=[{'label': i, 'value': i} for i in C.CONCENTRATION_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-filter", className="ml-auto")
            ),
        ],
        id="filter-modal",
        size="lg",
    ),
    html.P('Filters: None', id='filters-label', style={'font-style' : 'italic'})
], style={'width': '30%', 'display': 'inline-table', 'margin-top' : 20, 'margin-left' : 50}),

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
    Output('filter-modal', 'is_open'),
    Input('open-filter', 'n_clicks'),
    Input('close-filter', 'n_clicks'),
    State('filter-modal', 'is_open'))
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('filter-gender-dropdown', 'disabled'),
    Output('filter-race-ethnicity-dropdown', 'disabled'),
    Output('filter-bgltq-dropdown', 'disabled'),
    Output('filter-fgli-dropdown', 'disabled'),
    Output('filter-class-year-dropdown', 'disabled'),
    Output('filter-school-dropdown', 'disabled'),
    Output('filter-concentration-dropdown', 'disabled'),
    Input('axis', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def toggle_filters(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    filter_count = 0
    filter_enable_list = [False, False, False, False, False, False, False]
    filter_enable_list[C.VIZ_AXES.index(axis)] = True
    filter_disable_list = filter_enable_list.copy()

    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
    for i in range(len(filter_selections)):
        if filter_selections[i] == 'All':
            filter_disable_list[i] = (True)
        else:
            filter_count += 1

    if filter_count >= 2:
        return filter_disable_list
    return filter_enable_list

@app.callback(
    Output('filter-gender-dropdown', 'value'),
    Output('filter-race-ethnicity-dropdown', 'value'),
    Output('filter-bgltq-dropdown', 'value'),
    Output('filter-fgli-dropdown', 'value'),
    Output('filter-class-year-dropdown', 'value'),
    Output('filter-school-dropdown', 'value'),
    Output('filter-concentration-dropdown', 'value'),
    Input('axis', 'value'))
def reset_filters(axis):
    return ['All', 'All', 'All', 'All', 'All', 'All', 'All']

@app.callback(
    Output('filters-label', 'children'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def set_filters_label(gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    filter_str_list = []
    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
    for sel in filter_selections:
        if sel != 'All':
            filter_str_list.append(sel)
    
    if len(filter_str_list) == 0:
        return 'Filters: None'
    return 'Filters: ' + ', '.join(filter_str_list)

def filter_df(df, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    df = D.filter_gender(df, gender_filter)
    df = D.filter_race_ethnicity(df, race_ethnicity_filter)
    df = D.filter_bgltq(df, bgltq_filter)
    df = D.filter_fgli(df, fgli_filter)
    df = D.filter_class_year(df, class_year_filter)
    df = D.filter_school(df, school_filter)
    df = D.filter_conc(df, concentration_filter)
    return df

@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'),
    Input('course', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def update_graph(axis, course, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):        
    # get relevant dataframe according to axis
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter,
        fgli_filter, class_year_filter, school_filter, concentration_filter)
    keys = dff[axis].unique()

    df_list = []
    for key in keys:
        df_list.append(dff.loc[dff[axis] == key])
    
    dict_df = create_dict(course, df_list, keys)
    print(dict_df)
    
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
    
    print(percentages)

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